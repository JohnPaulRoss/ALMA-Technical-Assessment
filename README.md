Install the contents of this folder

For the following commands, I have assumed you are using a recent version of a debian based linux e.g. ubuntu 20.04 64 bit. You may need a different set of commands if you are using different versions of the OS.

Install some pre-requisites if necessary:

  sudo apt update
  sudo apt install python3 python3-venv python3-pip curl libcurl4-openssl-dev libssl-dev tar git

Install geckodriver:
  mkdir -p ~/bin
  cd ~/bin
  curl -L https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz | tar xz


Restart your shell to ensure your path is reloaded (note if you are running under a windowing environment like gnome you may need to restart the environment)
verify that geckodriver is in your path. If it isn’t ensure your PATH has ~/bin in it. Check it with:

  geckodriver --version

Clone the test code repository:
  cd
  git clone https://github.com/JohnPaulRoss/ALMA-Technical-Assessment.git

Create and activate a virtual environment to run the assessment (for example):
  python3 -m venv ~/virtualenvs/ALMA
  source ~/virtualenvs/ALMA/bin/activate
  cd ~/ALMA-Technical-Assessment
  chmod +x selenium_framework.py


Selenium tests

You can now run the sample framework as follows:

./selenium_framework.py

To get help:
./selenium_framework.py --help

The following parameters are supported all are optional:

  -h --help           display help
  --browser BROWSER   browsert to emulate
  --field-id FIELD_ID This allows you to change the field to be searched on
                      The default is search-input-mous but any of the search fields could be specified
  --field-value FV    This allows you to specify the field value to enter
                      to enter in the search field. The default is set to
                      a random existing value (uid://A002/X639a2a/X2a)
  --minimum-results   These two parameters allow you to set a minimum
  --maximum-results   and maximum expected result. Both these values
                      default to 1.
  --test-type         Type of test to run (default = ob-search). In future
                      the framework would support other types of test.
  --url URL           The base url to use defaults to https://almascience.eso.org/asax
  --platform PLATFORM The platform to use (linux, mac, android) default is linux
  --device-type DT    The device type to simulate (desktop, smartphone, tablet)

The program will use a useragent to emulate the required configuration
based on the provided browser, platform and device-type parameters.
If the combination specified is not allowed an error will be output
and the default of linux, firefox will be used.

So for example if you issue the command
./selenium_framework.py --minimum-results 2 --maximum-results 2

you will get the results:

Test results:
Step passed: Successfully set search criteria
Step failed: Expected at least 2, got 1 in observation panel
Overall test result Fail

That is, the results of each of the main steps in the test are logged and reported, It is anticipated that this could be used to generate automatic resports

P2API tests
These can be run as follows.

  python3 -m venv ~/virtualenvs/ALMA
  source ~/virtualenvs/ALMA/bin/activate
  cd ~/ALMA-Technical-Assessment
  chmod +x api_tests.py
  ./api_tests.py

  There are no parameters it runs some of the identified tests (some of the identified tests have not been implemented). These are:

  fc_test_001 Success status_code returns status code 204
  fc_test_002 Index too low returns status code 400
  fc_test_003 Index too high returns status code 400
  fc_test_004 Index does not exist returns status code 404

  The following test cases have not been implemented/

  fc_test_005 Not authenticated returning status code 401
  fc_test_006 No permission returning status code 403
  fc_test_007 Migration required returning status code 409

  possibly other tests for 400 status code.

  Implementation notes. See comment for more detailed information. It proved overly difficult to create obs in the way described in the specification document. I managed to make the api fail with a 500 error.
  Details are given in the code. I was unsure whether this was a problem with my test code or an actual bug in the api code. As it did not affect
  the actual running of the tests I chose to use the p2api package to create both OBs and finding charts. I then used the correct api to delete
  the finding charts created.

  Note these tests do not properly clean up after themselves so that need adding.

  I chose to use python and code the requests myself, rather than other industry tools like Postman. The reasoning for this is that it makes it easier to make tests do exactly what you want including having well defined test specs in (for example) yaml files or a database and storing the results in and generate reports from the database. (reword the stuff before.)
