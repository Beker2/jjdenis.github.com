#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import subprocess
import re
import time
import codecs
import os

def probamos():
    """
    """
    i = 0
    for orig_fn in os.listdir('inicial'):
        if orig_fn[-3:] != 'rst':
            continue
        print 'procesando {}'.format( orig_fn )
        subprocess.Popen('pandoc  -f rst -t markdown -o {}  inicial/{}'.format('intermedio.md', orig_fn),
                 stdout = subprocess.PIPE,
                 stderr = subprocess.PIPE, 
                 shell=True)
        time.sleep(0.5)
        interm_f = codecs.open('intermedio.md',"r", 'utf-8')
        lineas = interm_f.readlines()
        
        #cambia el título
        if (len(lineas[0]) == len(lineas[1])) and lineas[1][0] == u'=':
            lineas[0] = u'title:    {}'.format(lineas[0])
            lineas.pop(1)

        #línea blanca bajo el título
        if lineas[1] == '\n':
            lineas.pop(1)
        # tags
        for i, linea in enumerate(lineas):
            if linea[0:3] == u'  ~':
                lineas[i]   = lineas[i][3:]
                lineas[i-1] = (lineas[i-1][0:-1] + ':').ljust(9)

        #línea blanca bajo date
        if lineas[3] == '\n':
            lineas.pop(3)

        for i, linea in enumerate(lineas):
            if linea[0:4] == u'> \`':
                lineas[i]  = lineas[i][4:]
            if linea[-5:] == u'\`\_\n':
                lineas[i]  = lineas[i][:-5]+'\n'

        # * means "zero or more"; + means "one or more"; ? means "zero or one". 
        # \d = 1 digito  \s espacio
        
        p = re.compile(ur'\?w=\d+')
        
        for i, linea in enumerate(lineas):
            print linea[:-1]
            m = p.search(linea)
            lineas[i]=p.sub('?w=400', lineas[i])
            if m:
                print m.group()

            
        for i, linea in enumerate(lineas):
            if linea == u'[See the full gallery on\n':
                lineas.pop(i+1)
                lineas.pop(i)

        for i, linea in enumerate(lineas):
            if linea[0:4] == u'> ![':
                lineas[i] = lineas[i][2:]


        for i, linea in enumerate(lineas):
            lineas[i]=lineas[i].replace(u'\_', u'_')  



        #línea blanca bajo date
        if lineas[-1] == '\n':
            lineas.pop(-1)
        if lineas[-1] == '\n':
            lineas.pop(-1)


            
        final_fn = 'fuente/'+orig_fn[0:-4]+'.md'
        final_f = codecs.open(final_fn,"w",'utf-8')
        for linea in lineas:
            final_f.write( linea )
        
        interm_f.close()
        final_f.close()
        
        print final_fn
        #sys.exit()

probamos()