import pandas as pd
import datetime as dt
import os

from src.log import create_logger


logger = create_logger()


def read_plans(path):
	"""Read all the individual plans, and append them together.
	
	Args:
		path (str): Directory which contains the reports.
		
	Returns:
		pandas.DataFrame:
			Columns: Hónap, Ember, FTE, Projekt, Terv dátum
			
	"""
	
	try:
		files = os.listdir(path)
	except Exception as e:
		logger.error('File path {} doesn\'t exists, can\'t read plans.'.format(path))

	if len(files) == 0:
		raise ValueError('No input files found in {}.'.format(path))

	database = []
	for file in files:
		if file.endswith('.xlsx'):
			try:
				data_raw = pd.read_excel(os.path.join(path, file), skiprows=5, index_col=0)
				data = data_raw.transpose()

				data = data.loc[:, ~data.columns.isna()]
				data.reset_index(drop=True, inplace=True)
				data.drop(columns='Összesen (nap)', inplace=True)
				data.rename(columns={'Hónap kezdő dátum:': 'Hónap'}, inplace=True)
				data = data.melt(id_vars=['Hónap'], var_name='Ember', value_name='FTE')

				data['FTE'] = pd.to_numeric(data['FTE'], errors='coerce')
				data = data[data.FTE > 0]

				data['Projekt'] = file.split('.')[0]
				data['Terv dátum'] = dt.date.today()
				database.append(data)
				
			except Exception as e:
				logger.warning('Can\'t process {}.'.format(file))
				logger.warning(e)

	if len(database) > 0:
		database = pd.concat(database)
	
		return database

	else:
		raise ValueError('No useful data found in the dictionary.')
