import sys
import logging
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import boto.ec2
    from boto.exception import EC2ResponseError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logging.basicConfig(format='%(message)s (%(levelname)s)',
                    level=logging.INFO)
logging.getLogger('boto').propagate = False
boto.set_file_logger('boto', '/tmp/mc-control.log')

class EC2Instance():
    def __init__(self):
        try:
            from settings import *
        except ImportError:
            message = "Settings file doesn't exist.\n\n" \
                      "Copy settings.py.sample to settings.py and " \
                      "change its values"
            logging.warning(message)
            raise InstanceException(message)
        self.instance_id = INSTANCE
        self.conn = boto.ec2.connect_to_region(
            REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        

    def get_instance(self):
        try:
            self.inst = self.conn.get_only_instances(instance_ids=self.instance_id)[0]
        except EC2ResponseError, e:
            message = "Instance %s not found. Double check instance id "\
                      "in settings" % self.instance_id
            logging.error(message)
            raise InstanceException(message)

    def status(self):
        self.get_instance()
        return self.inst.state

    def toggle(self):
        current_status = self.status()
        if current_status == 'running':
            self.inst.stop()
            return "Stopping..."
        elif current_status == 'stopped':
            self.inst.start()
            return "Starting..."
        else:
            return "Please try again when the server is stopped or running"
        




class InstanceException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
