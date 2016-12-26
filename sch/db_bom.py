#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from sch import *
import argparse
import sys
import sqlite3
import re

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

parser = argparse.ArgumentParser(description='This script creates bom from the schematics and thedatabase.')
parser.add_argument('sch_file', nargs='+')
parser.add_argument('-d', '--db_file', help='filename of the database', action='store', required=True)
args = parser.parse_args()

db_conn = sqlite3.connect(args.db_file)
db_conn.row_factory = sqlite3.Row
db_cursor = db_conn.cursor()

out_list = []

for f in args.sch_file:

    eprint ("\nProcessing file '" + f + "' ...\n")

    sch = Schematic(f)
    
    for component in sch.components:
        # check if is power related component
        if '#PWR' in component.fields[0]['ref'] or\
           'PWR_FLAG' in component.fields[1]['ref']:
            continue

        # check for units. Do the processing only for the first unit (Ex. U301a)
        unit = component.unit['unit']
        if int(unit) != 1:
            eprint("Skipping unit " + component.unit['unit'])
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
                eprint("Found ID " + str(comp_id) + ' for \'' + comp_ref + '\'.')
                break

        if comp_id != 0:
            comp_id_t = (comp_id,)

            db_cursor.execute('SELECT * FROM source WHERE dev_id=?', comp_id_t)
            source_row=db_cursor.fetchone()
            if source_row==None:
                eprint ('No data found for \'' + comp_ref + '\'.')
            else:
                supplier=source_row['sup_id']
                ord_code=source_row['ordering_code']
                price=source_row['uprice']
                ppu=source_row['ppu']

                #get the name of the supplier
                supplier_t=(supplier,)
                db_cursor.execute('SELECT * FROM supplier WHERE id=?', supplier_t)
                supplier_row=db_cursor.fetchone()
                supplier_name=supplier_row['name']

                eprint("\tsupplier name '" + supplier_name + "'")
                eprint("\tunit price " + '%d' % price)
                eprint("\tpart per unit " + str(ppu))
                eprint("\tordering code '" + ord_code + "'")

                #Seek for the id. If not found insert.
                item=filter(lambda person: person['id'] == comp_id, out_list)
                if not item:
                    out_list.append({'id': comp_id, 'ordering_code': ord_code, 'count': 1, 'refdes': comp_ref, 'name': supplier_name, 'supplier_id': supplier, 'price': price, 'ppu': ppu })
                else: #update
                    oi=out_list.index(item[0])
                    count=out_list[oi]['count']
                    out_list[oi]['count']=count+1
                    refdes_list=out_list[oi]['refdes']
                    out_list[oi]['refdes']=refdes_list + ", " + comp_ref
#                print(out_list)
                

#    sch.save()

db_cursor.close()

print ("#id, supplier name, supplier id, count, refdes's, ordering code, price, subtotal")

total=0

for i, val in enumerate(out_list):
    dev_price=val['price'] / val['ppu']
    subtotal=val['count'] * dev_price
    total+=subtotal
    print(str(val['id']) + ", " + val['name'] + ", " + str(val['supplier_id']) + ", " + str(val['count']) + ", \"" + val['refdes'] + "\", " + val['ordering_code'] + ", " + str(dev_price) + ", " + str( subtotal))

print(",,,,,,total:, " + str(total))
