import sys
import logging
import warnings
import urllib2
import socket

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import boto.ec2
    from boto.exception import EC2ResponseError

try:
    from settings import *
except ImportError:
    message = "Settings file doesn't exist.\n\n" \
              "Copy settings.py.sample to settings.py and " \
              "change its values"
    logging.warning(message)
    raise InstanceException(message)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s ',
                    filename=LOG_FILE_PATH,
                    level=logging.INFO)
logging.getLogger('boto').propagate = False
boto.set_file_logger('boto', LOG_FILE_PATH)

class EC2Instance():
    def __init__(self):
        self.instance_id = INSTANCE
        self.conn = boto.ec2.connect_to_region(
            AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        self.last_status = "<app start>"

    def get_instance(self):
        try:
            self.inst = self.conn.get_only_instances(instance_ids=self.instance_id)[0]
        except EC2ResponseError, e:
            message = "Instance %s not found. Double check instance id "\
                      "in settings" % self.instance_id
            logger.error(message)

    def status(self):
        self.get_instance()
        status = self.inst.state
        if status == 'running' and self.last_status != 'running':
            logging.info("Server up, checking %s" % HTTP_ENDPOINT)
            try:
                response = urllib2.urlopen(HTTP_ENDPOINT, None, 2.5)
            except urllib2.URLError, e:
                logger.warning("URLError caught (%s)" % e.reason)
                status = 'pending'
            except socket.timeout:
                logger.warning("Socket timeout caught")
                status = 'pending'
        if status != self.last_status:
            logger.info("Status changed from %s to %s"
                         % (self.last_status, status))
            self.last_status = status
        return status

    def toggle(self):
        current_status = self.status()
        if current_status == 'running':
            self.inst.stop()
            logger.info("Stopping server.")
            return "Stopping..."
        elif current_status == 'stopped':
            self.inst.start()
            logger.info("Starting server.")
            return "Starting..."
        else:
            return "Please try again when the server is stopped or running"

class InstanceException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
