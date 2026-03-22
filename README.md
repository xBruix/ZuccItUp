# Zucc It Up
The Kirby Space Program's project for CSCI 375. Zucc It Up is a food delivery system for the VIU campus.

## Setting Up The Python Virtual Environment

The program must be run from inside a [Python virtual environment](https://www.w3schools.com/python/python_virtualenv.asp).

To create a virtual environment, you will need the following dependencies installed (these are already installed on the lab machines):
- python3 version 3.8 or later
- pip

If these are already installed, navigate to the project directory ZuccItUp/, then follow these steps:

#### 1. Create Virtual Environment

`python3 -m venv ./venv`

#### 2. Activate the Environment

`source ./venv/bin/activate`

After this, you should be able to see that you are working in the virtual environment because your command line will look something like this:

```
(venv) ...$
```

#### 3. Install All Required Packages

`pip install -r requirements.txt`

You are now able to run _pymongo_! I mean _pymango_!

### Important Reminder:

To run any Python file, you must run it from inside the virtual environment. Steps 1 and 3 are only necessary to _set up_ the environment, so they only need to be run once and never again. However, you will need to follow [step 2](#2-activate-the-environment) each time before you attempt to run a Python file.

## Setting Up The Database

1. Navigate to the DatabaseSetup directory with `cd DatabaseSetup/`.

2. Run `python3 DB_validation.py` to apply a schema validation to the three collections in the database (user, menu, and order). 

3. For step 3, you have two options: initialize all the collections, or initialize only one collection at a time.
   1. **To initialize all the collections at once**, run `python3 DB_init.py` and follow the prompts to enter your MangoDB username and password.
   2. **Initialize only one collection at a time**, run `python3 DB_<collection>.py`, where _\<collection\>_ is the name of one of the three collections (user, menu, or order).

The database is now filled with data!

