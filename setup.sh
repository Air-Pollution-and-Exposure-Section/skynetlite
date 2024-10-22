#!/bin/bash

# Define the file name
FILENAME="skynet/database/config.py"

# Create the file using the variable
touch $FILENAME

# Append configuration to the file
echo "### DATABASE LOCAL BUILD" >> $FILENAME
echo "DBNAME = 'DBNAME'" >> $FILENAME
echo "USER = 'DBUSER'" >> $FILENAME
echo "PASSWORD = 'USER_PASSWORD'" >> $FILENAME
echo "HOST = 'HOST'" >> $FILENAME
echo "PORT = 'PORT'" >> $FILENAME
echo "" >> $FILENAME
echo "DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'" >> $FILENAME
echo "" >> $FILENAME
echo "# PURPLEAIR READ KEY, WRITE KEY, GROUP ID" >> $FILENAME
echo "PA_READ_KEY = 'YOUR-READ-KEY'" >> $FILENAME
echo "PA_WRITE_KEY = 'YOUR-WRITE-KEY'" >> $FILENAME
echo "GROUP_ID = 'YOUR-GROUP-ID'" >> $FILENAME
echo "" >> $FILENAME
echo "# AQEGG API KEY" >> $FILENAME
echo "AQEGG_API_KEY = 'YOUR-API-KEY'" >> $FILENAME 
