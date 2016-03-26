# EC2 App

Python/Tkinter script to start and stop a single EC2 instance.

## Set Up

This does not work out of the box. You need to configure your python
environment and you need to specify your Amazon Web Services (AWS)
information.

### Python environment

You need to install the
[boto Python library](http://boto.cloudhackers.com/en/latest/) for
communicating with AWS. The best way to do this is with
[`virtualenv`](https://virtualenv.pypa.io/en/latest/).

Assuming you have `virtualenv` installed, do the following in the
directory where you've checked this out:

    $ virtualenv env                  # create the virtual environment
    $ . env/bin/activate              # activate the environment
    $ pip install -r requirements.txt  # install boto, et al.

### Settings

The main script uses `settings.py` to identify the AWS region,
instance id, and authentication credentials - but this file doesn't
exist in the git repository. Copy the `settings.py.sample` to
`settings.py` and edit.

* `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`: Credentials to
   connect to AWS.
* `AWS_REGION`: Identification string for the region where the
   instance runs.
* `INSTANCE`: The instance id for the instance to control.
* `HTTP_ENDPOINT`: A URL to check to confirm that the EC2 instance is
   fully running. See more below.
* `LOG_FILE_PATH`: Path to a log file.

AWS reports that the instance is running before all of its services
and daemons have started up. Since my use case (and many others) is to
run a web service on the instance, this app requests the URL in the
`HTTP_ENDPOINT` setting and confirms that the instance is running when
this request returns HTTP status 200.

## Running

You can run from the directory by typing:

    $ python main.py

Build into a mac app using
[PyInstaller](https://pythonhosted.org/PyInstaller/) like this:

    $ pip install PyInstaller       # only need to do this once
    $ pyinstaller -n "EC2 App" -i app.icns -w main.py

## Background

In putting together a Minecraft server running on a small EC2
instance, I wanted to give my son an easy way to start the instance
remotely.
