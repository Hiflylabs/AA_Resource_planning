import pandas as pd
import datetime as dt
import re

from pdb import set_trace


def create_report(database):
	"""Creates a resource report based on the most recent plans.
	
	Args:
		database (pandas.DataFrame): All historical plans
		
	Returns:
		pandas.DataFrame
	
	"""

	# The most recent plan for all projects
	report = (
		database.sort_values(['Hónap', 'Ember', 'Projekt', 'Terv dátum'])
		.drop_duplicates(['Ember', 'Projekt', 'Hónap'], keep='last')
	)
	set_trace()
	# Keep only the current and the upcoming months
	report = report[report['Hónap'] > (report['Terv dátum'] - dt.timedelta(days=30))]

	# Filter and transform columns
	report = report[['Ember', 'Projekt', 'Hónap', 'FTE', 'Terv dátum']]
	report['Év'] = report['Hónap'].dt.year
	report['Hónap'] = report['Hónap'].dt.month
	report['FTE'] = report['FTE'].round(3)
	report['Projekt'] = report['Projekt'].apply(clean_project_name)
	report.sort_values(['Projekt', 'Ember', 'Év', 'Hónap', 'FTE', 'Terv dátum'], inplace=True)

	# Create a separate row for all employee & project combination
	report = report.pivot_table(
		values=['FTE'],
		index=['Ember', 'Projekt'],
		columns=['Év', 'Hónap'],
		aggfunc=sum,
		fill_value=0
	)
	report.columns = [str(c[1]) + str(c[2]).rjust(2, '0') for c in report.columns]
	report.reset_index(inplace=True)
	report.sort_values(['Projekt', 'Ember'], ignore_index=True, inplace=True)

	return report


def clean_project_name(name):
	"""Get project name from the file name."""

	name = name.replace('_', ' ')
	name_splitted = name.split(' ')

	if re.match('\d{8}$', name_splitted[-1]):
		return ' '.join(name_splitted[:-1])

	else:
		return name
