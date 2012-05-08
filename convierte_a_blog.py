#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import subprocess
import re
import time
import codecs
import os
import unicodedata
import Image
import ExifTags
import sys
import datetime
import random

DIR_IMAGENES_ORIGEN   = 'imagenes_borrador/'
DIR_IMAGENES_LOCAL    = 'static/'

SITE_ROOT    = os.path.dirname(os.path.realpath(__file__))
LINK_STATIC_WEB = 'http://axaragua.github.com/static/' 
LINK_STATIC_LOCAL = 'file://'+SITE_ROOT+'/'+ DIR_IMAGENES_LOCAL


def pregunto():
    titulo = raw_input("Enter para actualizar, p para publicar, o un título para archivo nuevo: ").decode(sys.stdin.encoding)

    if titulo == 'p':
        publica_en_github()

    elif titulo != '':
        creo_nuevo_articulo(titulo)
    elif titulo == '':
        actualiza_imagenes()
        ejecuta_pelican()
        abre_firefox()


def publica_en_github():
    a = os.listdir('.')
    archivos_md = [n for n in a if n[-3:] == '.md' and n !='intermedio.md']

    for archivo_md in archivos_md:
        print 'procesando {}'.format(archivo_md)

        m = codecs.open(archivo_md, 'r', 'utf-8')
        lines = m.readlines()
        print LINK_STATIC_LOCAL, LINK_STATIC_WEB
        
        for i,l in enumerate(lines):
            lines[i] = lines[i].replace(LINK_STATIC_LOCAL, LINK_STATIC_WEB)
            print lines[i],
        m.close()

        m = codecs.open(archivo_md, 'w', 'utf-8')
        m.write(u''.join(lines))
        m.close()
        
        os.rename(archivo_md, 'fuente/'+archivo_md)
    ejecuta_pelican()
        
    

def actualiza_imagenes():
    a = os.listdir(DIR_IMAGENES_ORIGEN)
    archivos_imagen = [n for n in a if n[-4:] in ['.jpg', 'jpeg', '.JPG']]

    if archivos_imagen:
        a = os.listdir(SITE_ROOT)
        archivos_md = [n for n in a if n[-3:] == '.md' and n !='intermedio.md']
        if len(archivos_md) > 1:
            print "varios archivos md, no se en cual poner la imagen"
        elif len(archivos_md) == 1:
            num_imagen = random.randrange(100, 1000, 10)
            texto = u''
            titulo = archivos_md[0][0:-3]
            titulo = titulo.decode('utf-8')
            for nombre_imagen in archivos_imagen:
                referencia, link1 = procesa_imagen(nombre_imagen, titulo, num_imagen)
                texto += referencia
                texto += link1
                num_imagen+=1

            print texto

            salida = codecs.open(archivos_md[0], 'a', 'utf-8')
            salida.write('\n')
            salida.write(texto)
            salida.close()
            
            abre_en_textmate(archivos_md[0])

    


def creo_nuevo_articulo(titulo):
    """
    """
    titulo = titulo.lstrip().rstrip()
    articulo  = u'title:     {}\n'.format(titulo)
    articulo += u'date:      {}\n'.format(datetime.datetime.today().strftime('%Y-%m-%d %H:%M'))
    articulo += u'category:  {}\n\n'.format('General')
    links = u''
    
    a = os.listdir(DIR_IMAGENES_ORIGEN)
    archivos_imagen = [n for n in a if n[-4:] in ['.jpg', 'jpeg', '.JPG']]
    num_imagen = 1
    for nombre_imagen in archivos_imagen:
        
        referencia, link1 = procesa_imagen(nombre_imagen, titulo, num_imagen)

        articulo += referencia
        links += link1

        num_imagen+=1
    
    print articulo
    print links

    nombre_salida_md = osifica(titulo) + '.md' # título viene del principio, de raw_input
    salida = codecs.open(nombre_salida_md, 'w', 'utf-8')
    salida.write(articulo)
    salida.write('\n')
    salida.write(links)
    salida.close()
    
    ejecuta_pelican()
    abre_en_textmate(nombre_salida_md)
    abre_firefox()

def ejecuta_pelican_en_terminal():
    a=subprocess.Popen("""osascript -e 'tell application "Terminal" to do script "cd {} ; pelican -o web -m md -s pelican.conf.py ."' """.format(SITE_ROOT),
         stdout = subprocess.PIPE,
         stderr = subprocess.PIPE, 
         shell=True) #pelican -o web -m md -s pelican.conf.py .

def ejecuta_pelican():
    a=subprocess.Popen("pelican -o web -m md -s pelican.conf.py .",
         stdout = subprocess.PIPE,
         stderr = subprocess.PIPE, 
         shell=True) #pelican -o web -m md -s pelican.conf.py .

def git_commit(mensaje):
    a=subprocess.Popen("git commit -a -m '{}'".format(mensaje),
         stdout = subprocess.PIPE,
         stderr = subprocess.PIPE, 
         shell=True) #pelican -o web -m md -s pelican.conf.py .

def git_commita(mensaje):
    a=subprocess.Popen("""osascript -e 'tell application "Terminal" to do script "cd {} ; git commit -a -m {}"' """.format(SITE_ROOT, mensaje),
         stdout = subprocess.PIPE,
         stderr = subprocess.PIPE, 
         shell=True) #pelican -o web -m md -s pelican.conf.py .

"""osascript -e 'tell application "Terminal" to do script "cd {} ; pelican -o web -m md -s pelican.conf.py ."' """.format(SITE_ROOT),
         


def abre_firefox():
    a=subprocess.Popen('open -a firefox web/index.html',
         stdout = subprocess.PIPE,
         stderr = subprocess.PIPE, 
         shell=True)
         
def abre_en_textmate(archivo):
    a=subprocess.Popen('open -a textmate {}'.format(archivo),
         stdout = subprocess.PIPE,
         stderr = subprocess.PIPE, 
         shell=True)



    
# probamos



def procesa_imagen(nombre_imagen, titulo, num_imagen):

    print 'procesando {}'.format( nombre_imagen )
    
    titulo_imagen = ''.join(nombre_imagen.split('.')[0:-1])
    titulo_imagen = titulo_imagen.decode('utf-8')
    titulo_imagen = unicodedata.normalize('NFD', titulo_imagen).encode('ascii','ignore')
    titulo_imagen = unicode(titulo_imagen)
    
    print titulo_imagen, type(titulo_imagen)

    nuevo_nombre_imagen          = osifica(titulo) + '_' + osifica(titulo_imagen) +'.jpg'

    im = Image.open(DIR_IMAGENES_ORIGEN + nombre_imagen)

    # Rota la imagen según lo que diga la información exif
    for orientation in ExifTags.TAGS.keys() :
        if ExifTags.TAGS[orientation]=='Orientation' : break 
    exif=dict(im._getexif().items())

    print exif[orientation]
    
    if  exif[orientation] == 3 : 
        im=im.transpose(Image.FLIP_TOP_BOTTOM)
        im=im.transpose(Image.FLIP_LEFT_RIGHT)
    elif exif[orientation] == 6 : 
        im=im.transpose(Image.ROTATE_270)
    elif exif[orientation] == 8 : 
        im=im.transpose(Image.ROTATE_180)


    # Creo la imagen
    im_grande = im.copy()
    im_grande.thumbnail( (960, 960), Image.ANTIALIAS)
    im_grande.save( DIR_IMAGENES_LOCAL + nuevo_nombre_imagen)



    #referencia ='### {}\n'.format(nombre_imagen) 
    # Crea el link en el texto 
    # [![anita lectora][1]][2]
    referencia += u'[![{}][{}]][{}]\n'.format(
        titulo_imagen, num_imagen, num_imagen
        )
    
    # Crea los link de origen de las imágenes
    #[1]: file:///Users/jjdenis/axaragua.github.com/imagenes_local/a_ver_aveeeer_anita_lectora.jpg 
    link1 = u'[{}]: {}{} \n'.format(
        num_imagen, 
        LINK_STATIC_LOCAL,
        nuevo_nombre_imagen
        )

    os.rename(os.path.join(DIR_IMAGENES_ORIGEN, nombre_imagen),
                os.path.join(DIR_IMAGENES_ORIGEN, 'originales', nombre_imagen)
                )
       
    return referencia, link1


def osifica(cadena):
    cadena = cadena.replace(' ', '_')
    cadena = unicodedata.normalize('NFKD', cadena).encode('ascii','ignore')
    cadena = unicode(cadena)
    return cadena


pregunto()
