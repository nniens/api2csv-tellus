# API2CSV Tellus #

Python script to extract all data from https://api.data.amsterdam.nl/tellus into 1 CSV file.
This api can only be used if you are working in our organisation.
It uses a grant, refresh and access token.
The grant token is obtained with the login page of https://atlas.amsterdam.nl.

### Install procedure ###

```
git clone https://github.com/amsterdam/api2csv-tellus.git
virtualenv --python=$(which python3) venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python import_tellus.py

```
