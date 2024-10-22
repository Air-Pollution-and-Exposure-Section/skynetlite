#!/usr/bin/env python3
import os
import pandas as pd
import datetime


user = "jonathanlevine"
database = "skynet"


def get_today_date()->datetime.datetime:
	return datetime.datetime.now().strftime("%Y-%m-%d")


def execute_database_backup(database:str, user:str)->None:
	print("started: pg_dump -U {} {} > backups/{}_backup_{}.sql ...".format(user, database, database, get_today_date()))
	os.system("pg_dump -U {} {} > backups/{}_backup_{}.sql".format(user, database, database, get_today_date()))
	print("done.")



def remove_old_backups(num_days:int)->None:
	print("started: find backups -type f -mtime +14 -delete ...")
	os.system("find backups -type f -mtime +{} -delete".format(num_days)) 
	print("done.")


if __name__=="__main__":
	# BACKUP THE DATABASE
	execute_database_backup(database, user)
	# REMOVE BACKUPS THAT ARE 14 DAYS OLD
	remove_old_backups(14)