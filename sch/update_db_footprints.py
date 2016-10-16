#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from sch import *
import argparse
import sys
import sqlite3
import re

parser = argparse.ArgumentParser('This script updates the footprint and other fields of sch files using a database as input')
parser.add_argument('sch_file', nargs='+')
parser.add_argument('--db_file', help='filename of the database', action='store', required=True)
args = parser.parse_args()

db_conn = sqlite3.connect(args.db_file)
db_conn.row_factory = sqlite3.Row
db_cursor = db_conn.cursor()

for f in args.sch_file:
    sch = Schematic(f)
    
    for component in sch.components:
        # check if is power related component
        if '#PWR' in component.fields[0]['ref'] or\
           'PWR_FLAG' in component.fields[1]['ref']:
            continue
    
        # component reference
        comp_ref = component.fields[0]['ref'].replace('"', '')

        comp_id = 0

        # get the 'id' field
        for i, val in enumerate(component.fields):
            f_name = val['name']
            f_val = val['ref']
            #print (f_name)
            #print (f_val)
            if "id" in f_name:
                m = re.search('\d+', f_val)
                comp_id = int(m.group(0))
                print("Found ID " + str(comp_id) + ' for \'' + comp_ref + '\'.')
                break
        #get the row from the cad_data table
        if comp_id != 0:
            comp_id_t = (comp_id,)
            db_cursor.execute('SELECT * FROM cad_data WHERE cad_tool=2 AND dev_id=?', comp_id_t)
            cad_row=db_cursor.fetchone()
            if cad_row==None:
                print ('No cad data found for \'' + comp_ref + '\'.')
            else: #update things.
                if cad_row['footprint']==None:
                    footprint=""
                    print ('Warning! Empty footprint value in the database!')
                else:
                    footprint=cad_row['footprint']
                print ('Updateing footprint to \'' + footprint + '\'.')
                component.fields[2]['ref'] = '"' + footprint + '"'
            db_cursor.execute('SELECT * FROM device WHERE id=?', comp_id_t)
            dev_row=db_cursor.fetchone()
            if dev_row==None:
                print ('No device data found for \'' + comp_ref + '\'.')
            else:
                if dev_row['value']==None:
                    print ('Warning! Empty value string in the database!')
                    comp_value=""
                else:
                    comp_value=dev_row['value']
                print ('Updateing vale to \'' + comp_value + '\'.')
                component.fields[1]['ref'] = '"' + comp_value + '"'
        else:
            print ("No 'id' field found for '" + comp_ref + "'.")

    sch.save()

db_cursor.close()
