import pandas as pd
import datetime as dt
import os


def write_plans(plans, db_path, db_name):
	"""Appends the plans to the database.
	
	Actually, the database is a simple excel file.

	Args:
		plans (pandas.DataFrame): plans data
		db_path (str): Path to the DB file
		db_name (str): Name of the DB file

	"""

	db_full_name = os.path.join(db_path, db_name)

	# If the database already exists, append the new data.
	# The previous entries for the actual date will be overwritten.
	if db_name in os.listdir(db_path):
		database_old = pd.read_excel(db_full_name)
		database_old = database_old[database_old['Terv dátum'] < pd.to_datetime(dt.date.today())]
		database_full = pd.concat([database_old, plans])
		database_old.to_excel(os.path.join(db_path, 'backup', 'database_bkp.xlsx'))
		database_full.to_excel(db_full_name)

	else:
		plans.to_excel(db_full_name)


def read_database(db_path, db_name):
	"""Reads the database file and returns.
	
	Args:
		db_path (str): Path to the DB file
		db_name (str): Name of the DB file
		
	Returns:
		pandas.DataFrame
		
	"""

	return pd.read_excel(os.path.join(db_path, db_name))
