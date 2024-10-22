# skynet
![skynet](assets/skynet.jpg)

## Layout of the database
Docs are in development for the layout of the database. For the most recent schema of the database see [here](https://github.com/Air-Pollution-and-Exposure-Section/skynet/issues/17).

## Instructions
To setup the database, there are some dependencies that need to be installed (1) PostgrteSQL (2) skynet codebase (3) build the database.

### *** Note: for containerizing the ingesters and running them, only steps (2) and (5) are required. 

### Step 1: Installation and setup of PostgreSQL
See [here](https://www.devart.com/dbforge/postgresql/how-to-install-postgresql-on-linux/) for installing PostgreSQL on a linux machine (or VM).

See [here](https://mcengkuru.medium.com/how-to-install-psql-on-your-mac-a-step-by-step-guide-with-troubleshooting-tips-ade65c441abf) for installing PostgreSQL via macOS terminal.

For windows installation .... you're on your own!

After installing PostgreSQL, you'll need to create a new database and user. Can access the psql shell by writting this in a bash shell:
```bash
$ psql -U postgres -d postgres
```
If you get the following error `FATAL: Peer authentication failed for user "postgres"` see [here](https://stackoverflow.com/questions/18664074/getting-error-peer-authentication-failed-for-user-postgres-when-trying-to-ge) for the solution.

To create a new database and user do this in the psql shell:
```psql
# create database dev;
```
```psql
# create user myuser;
```
You may need to create a password for this user:
```psql
# alter user myuser with password <<PASSWORD>>;
```

### Step 2: Building skynet from source

The best way to install the skynet codebase and all the required packages is to build from source. Simply create a python3 virtualenv in the root dir of the repo:
```bash
$ python3 -m venv venv
```
Activate the virtualenv
```bash
$ source venv/bin/activate
```
Install:
```bash
$ pip install -e .
```

You can confirm that all the packages were installed properly by typing `$ pip list` in terminal. You should see this:
(Note that `user/apex` in `/Users/user/apex/skynet` will be different for you depending on the username of your system and the location of the skynet repo on your system)
```bash
Package            Version     Editable project location
------------------ ----------- ---------------------------
arrow              1.2.3
certifi            2024.2.2
charset-normalizer 3.3.2
idna               3.7
numpy              1.26.4
pandas             2.2.0
pip                24.0
psycopg2-binary    2.9.9
python-dateutil    2.9.0.post0
pytz               2024.1
requests           2.29.0
six                1.16.0
skynet             0.1.1       /Users/jonathan/apex/skynet
SQLAlchemy         2.0.25
typing_extensions  4.11.0
tzdata             2024.1
urllib3            1.26.18
```

### Step 3: Creating the config file

Additionally run the following in your bash shell:
```bash
$ bash setup.sh
```
To create your config file `database/config.py`.

For a local build of the skynet database, edit parameters `DBNAME`, `USER`, `PASSWORD`, `HOST`, `PORT`, in the config file database/config.py to something like this
```python3
DBNAME = 'dev'
USER = 'myuser'
PASSWORD = <<PASSWORD>>
HOST = 'localhost'
PORT = '5432'
```
For a build on FSDH or elsewhere, `DBNAME`, `USER`, `PASSWORD`, `HOST`, `PORT` will have to be changed accordingly. Can email jonathan.levine@hc-sc.gc.ca for help.

The PurpleAir and AQEGG API keys: `PA_READ_KEY`, `PA_WRITE_KEY`, `GROUP_ID`, `AQEGG_API_KEY` should also be set if running the `purpleair.py` and `aqegg.py` ingesters in `ingesters/`. In `database/config.py` placeholder variables are already set:
```
# PURPLEAIR READ KEY, WRITE KEY, GROUP ID
PA_READ_KEY = 'YOUR-READ-KEY'
PA_WRITE_KEY = 'YOUR-WRITE-KEY'
GROUP_ID = YOUR-GROUP-ID

# AQEGG API KEY
AQEGG_API_KEY = 'YOUR-API-KEY'
```
Email jonathan.levine@hc-sc.gc.ca for getting access to these API keys if you do not have them already.

### Step 4: Build the database

The build an instance of the database run (make sure the virtualenv is activated):
```bash
$ python3 build_db.py
```
You can confirm that the database was built with `\dt+` in the psql shell:
```
dev=# \dt+
                                               List of relations
 Schema |           Name           | Type  |  Owner   | Persistence | Access method |    Size    | Description 
--------+--------------------------+-------+----------+-------------+---------------+------------+-------------
 public | aq_egg_data              | table | myuser | permanent   | heap          | 8192 bytes | 
 public | channel_a_primary_data   | table | myuser | permanent   | heap          | 8192 bytes | 
 public | channel_a_secondary_data | table | myuser | permanent   | heap          | 8192 bytes | 
 public | channel_b_primary_data   | table | myuser | permanent   | heap          | 8192 bytes | 
 public | channel_b_secondary_data | table | myuser | permanent   | heap          | 8192 bytes | 
 public | co2                      | table | myuser | permanent   | heap          | 8192 bytes | 
 public | eahmu_hourly             | table | myuser | permanent   | heap          | 8192 bytes | 
 public | eahmu_minute             | table | myuser | permanent   | heap          | 8192 bytes | 
 public | endpoint                 | table | myuser | permanent   | heap          | 16 kB      | 
 public | exposure                 | table | myuser | permanent   | heap          | 8192 bytes | 
 public | field_data_codes         | table | myuser | permanent   | heap          | 16 kB      | 
 public | humidity                 | table | myuser | permanent   | heap          | 8192 bytes | 
 public | instrument               | table | myuser | permanent   | heap          | 80 kB      | 
 public | location                 | table | myuser | permanent   | heap          | 16 kB      | 
 public | microaeth_casap          | table | myuser | permanent   | heap          | 8192 bytes | 
 public | participant              | table | myuser | permanent   | heap          | 104 kB     | 
 public | participant_at_location  | table | myuser | permanent   | heap          | 8192 bytes | 
 public | participation            | table | myuser | permanent   | heap          | 80 kB      | 
 public | particulate              | table | myuser | permanent   | heap          | 8192 bytes | 
 public | pressure                 | table | myuser | permanent   | heap          | 8192 bytes | 
 public | purpleair_keys           | table | myuser | permanent   | heap          | 48 kB      | 
 public | raw_json                 | table | myuser | permanent   | heap          | 8192 bytes | 
 public | responsibility           | table | myuser | permanent   | heap          | 504 kB     | 
 public | sample                   | table | myuser | permanent   | heap          | 1432 kB    | 
 public | sample_data              | table | myuser | permanent   | heap          | 8192 bytes | 
 public | sample_data_codes        | table | myuser | permanent   | heap          | 480 kB     | 
 public | sample_from_instrument   | table | myuser | permanent   | heap          | 536 kB     | 
 public | site                     | table | myuser | permanent   | heap          | 16 kB      | 
 public | site_location            | table | myuser | permanent   | heap          | 8192 bytes | 
 public | study                    | table | myuser | permanent   | heap          | 16 kB      | 
 public | study_site               | table | myuser | permanent   | heap          | 8192 bytes | 
 public | substance                | table | myuser | permanent   | heap          | 72 kB      | 
 public | temperature              | table | myuser | permanent   | heap          | 8192 bytes | 
(33 rows)
```

### Step 5: Containerize the **ingesters** `purpleair.py` and `aqegg.py` with Docker
The **ingesters** dir contains two dirs, `purpleair` and `aqegg`. Each of these dirs have their respective Dockerfiles required for containering the respective ingester scripts.

As an example, to build the AQEgg ingester docker image, in the root of the repo type this in your bash terminal:
```bash
$ docker build -f ingesters/aqegg/Dockerfile -t aqegg-ingester-image .
```
To run the docker image type this in the terminal (Note that the `--network="host"` is required as we are directing the container to save API results to a database on the same system the container is running on):
```bash
$ docker run --rm --network="host" aqegg-ingester-image
```
