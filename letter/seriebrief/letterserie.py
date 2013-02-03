#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import os

con = lite.connect('datenbank')

ctr=0
lux_id = 1
os.system('cp letterpt1 seriebrief_template')
os.system('cp letterpt1 seriebrief')
os.system('cp collection seriebrief_sammlung')

with con:

    cur = con.cursor()
    for lux_id in range(1, 5):
        f = open('seriebrief', 'r+')
        f.seek(-1,2) 
        string = str("\n\n\Adresse{\n\t")
        for ctr in range(0, 5):
            sql = "SELECT vorname, nachname, adresse, plz, ort FROM member WHERE id=%d" %(10 * lux_id)
            cur.execute(sql)
            rows = [ a[ctr] for a in cur.fetchall()]
            for row in rows:
                print row
            string = string + str(row) + str(" ")
            if ctr == 1:
                string = string + str("\\\\\n")
            if ctr == 2:
                string = string + str("\\\\\n")
            ctr = ctr + 1
        string = string + str("}\n\n")
        f.write(string)
        f.close()
        f = open('letterpt2', 'r')
        string2 = f.read()
        string = str(string2)
        f.close()
        f = open('seriebrief', 'r+')
        f.seek(-1,2)
        f.write(string)
        f.close()
        filenames = str("cp seriebrief seriebrief_%d.tex") % (lux_id)
        os.system(filenames)
        os.system('rm seriebrief')
        os.system('cp seriebrief_template seriebrief')
        f = open('seriebrief_sammlung', 'r+')
        f.seek(-1,2)
        pdfname = str("\includepdf[pages=-]{seriebrief_%d.pdf}\n\n") % (lux_id)
        f.write(pdfname)
        f.close()
        
        lux_id = lux_id + 1 

os.system('for file in *.tex; do pdflatex "$file"; done') 
os.system('cp seriebrief_sammlung seriebrief_sammlung.tex')
f = open('seriebrief_sammlung.tex', 'r+')
f.seek(-1,2)
string = str("\end{document}")
f.write(string)
f.close()
os.system('pdflatex seriebrief_sammlung.tex')
os.system('rm *.aux && rm *.log')
        
