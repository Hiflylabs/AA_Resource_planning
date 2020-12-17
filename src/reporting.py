# -*- coding: utf-8 -*-
"""TS_planner

"""

import datetime as dt
import os

from src.readplans import read_plans
from src.dbmanager import write_plans, read_database
from src.createreport import create_report

try:
	path = './data'
	db_path = os.path.join(path, '_database')
	db_name = 'database.xlsx'

	formatted_date = dt.date.today().strftime(format="%Y%m%d")
	report_name = os.path.join(path, '_report', 'AA_RESOURCE_REPORT_{}.xlsx'.format(formatted_date))

	# Reads the plans and appends them to the database
	plans = read_plans(path)
	write_plans(plans, db_path, db_name)

	# Create report based on the last version of the plans
	database = read_database(db_path, db_name)
	report = create_report(database)
	report.to_excel(report_name)

except Exception as e:
	print(e)
