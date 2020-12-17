import pandas as pd
import datetime as dt
import os


def read_plans(path):
	"""Read all the individual plans, and append them together.
	
	Args:
		path (str): Directory which contains the reports.
		
	Returns:
		pandas.DataFrame:
			Columns: Hónap, Ember, FTE, Projekt, Terv dátum
			
	"""

	database = []
	for file in os.listdir(path):
		if file.endswith('.xlsx'):
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

	database = pd.concat(database)
	
	return database
