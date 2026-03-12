# Zucc It Up
The Kirby Space Program's project for CSCI 375. Zucc It Up is a food delivery system for the VIU campus.

## Setting up a python virtual environment

The program must be run from inside a [Python virtual environment](https://www.w3schools.com/python/python_virtualenv.asp).

To create a virtual environment, you will need the following dependencies installed (these are already installed on the lab machines):
- python3 version 3.8 or later
- pip

If these are already installed, navigate to the project directory ZuccItUp/, then follow these steps:

#### 1. Create Virtual Environment

`python3 -m venv ./venv`

#### 2. Activate the Environment

`source ./venv/bin/activate`

After this, you should be able to see that you are working in the virtual environment because your command line will something like this:

```
(venv) ...$
```

You can also run `ls` to list everything in your current directory, and you should see a directory called "venv".

#### 3. Install All Required Packages

`pip install -r requirements.txt`

You are now able to run _pymongo_! I mean _pymango_!