Machine Learning for Python Programmers
=======================================

Getting Started
---------------

MongoDB Setup
.............

1. Install MongoDB 3. On Linux or Windows you're on your own. On OS X::

    $ brew install mongodb

   *Note*: Double check that you've got version 3 with::

    $ mongod --version
    db version v3.0.7

   If you have an older version, update with::

    $ brew unlink mongodb
    $ brew install mongodb

2. Start MongoDB. On OS X::

    $ mongod --config /usr/local/etc/mongod.conf

3. Install a GUI. We like Robomongo, available for Windows, Linux, and OS X:
   http://robomongo.org/


Python Setup
............

1. Setup a Python virtual environment::

    $ virtualenv env

2. Activate the Python virtual environment (note: you'll need to do this each
   time you open a new shell)::

    $ . env/bin/activate

3. Install the requirements::

   $ pip install -r requirements.txt

4. Run the system-test notebook by running ``ipython notebook``, clicking
   ``system-test.ipynb``, clicking *Cell* -> *Run All*, and making sure
   there are no errors::

   $ ipython notebook
