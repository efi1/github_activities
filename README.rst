=================
Github assignment
=================

This assignment validating various Github activities using GitPython API

Usage:

    python setup.py install (please run it first)

    all testing variables resides in settings.py under tests folder

    they can updated directly at the settings.py or can alternatively used by the command line as flags.

    e.g. python -m pytest --token <token hush>

    if not using a flag for a certain variable it will be taken from the setting.py


it is important to update the token variable with the relevant one (or use the flag) before running.

the token is a Github token which should be generate in your Github account and should contains

some admins permissions which required to perform the activities within the tests.

under src.clients you may find the test_client.py
it is based on the git packages and contains the major activities of which the test cases use.

test execution will write into a log file logfile.log (under tests folder) as well it prints the
running log to the console.

you may use an html flag (it uses the pytest-html packaged which is installed by setup.py).
at the end of the run a report.html file is created under the project folder and can be opened in a web browser.
to use it:
python -m pytest --html=report.html



