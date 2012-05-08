#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import subprocess
import re
import time
import codecs
import os
import requests
import Image
import StringIO
import ExifTags
import sys

SITE_ROOT    = os.path.dirname(os.path.realpath(__file__))
DIR_IMAGENES_LOCAL    = 'static/'
LINK_STATIC_LOCAL = 'file://'+SITE_ROOT+'/'+ DIR_IMAGENES_LOCAL

def probamos():
    """
    """
    i = 0
    
    
    for orig_fn in os.listdir('inicial'):
        print 'procesando {}'.format( orig_fn )
        f = codecs.open('inicial/'+orig_fn,"r", 'utf-8')
        lineas = f.readlines()
        links = ''
        
        num_3l = 0
        i = 0


        while True:
            if num_3l == 2:
                break
            if lineas[i].startswith('---'):
                num_3l +=1
                lineas.pop(i)
                continue
            elif lineas[i].startswith(('layout:', 
                                       '- ',
                                       'status:',
                                       'wordpress_id:',
                                       'post_format:',
                                       'tags:',
                                       )):
                lineas.pop(i)
                continue
            else:
                i+=1
        
        i=0
        while True:
            if i+1 >= len(lineas):
                break
            if lineas[i]=='\n' and lineas[i+1]=='\n':
                lineas.pop(i+1)
            else:
                i+=1

        for i, linea in enumerate(lineas):
            if lineas[i].startswith('date:'):
                lineas[i]=lineas[i].replace("'", "")



        p = re.compile(
                       ur'\!\[(.*?)\]\((http://.+?)\)'
                       )
        k = 1
        num_imagen = 1
        links = ''
        referencia = ''
        for i, linea in enumerate(lineas):

            m = p.search(linea)
            if not m:
                continue
            
            #print m.group(1)
            direcc = m.group(2)
            r = requests.get(direcc)
            if r.headers['content-type'] == 'image/jpeg':

                im = Image.open(StringIO.StringIO(r.content))
                
                # Rota la imagen según lo que diga la información exif
                for orientation in ExifTags.TAGS.keys() :
                    if ExifTags.TAGS[orientation]=='Orientation' :
                        if  im._getexif():
                            exif=dict(im._getexif().items())
                            if orientation in exif:
                                print exif[orientation]

                                if  exif[orientation] == 3 : 
                                    im=im.transpose(Image.FLIP_TOP_BOTTOM)
                                    im=im.transpose(Image.FLIP_LEFT_RIGHT)
                                elif exif[orientation] == 6 : 
                                    im=im.transpose(Image.ROTATE_270)
                                elif exif[orientation] == 8 : 
                                    im=im.transpose(Image.ROTATE_180)
                        break 
                nombre_foto = orig_fn[:-9]+'_foto'+str(k)+'.jpg'
                im.save(DIR_IMAGENES_LOCAL+nombre_foto,"JPEG")

            elif r.headers['content-type'] == 'image/png':
                im = Image.open(StringIO.StringIO(r.content))
                nombre_foto = orig_fn[:-9]+'_foto'+str(k)+'.png'
                im.save(DIR_IMAGENES_LOCAL+nombre_foto,"png")
            elif r.headers['content-type'] == 'image/gif':
                im = Image.open(StringIO.StringIO(r.content))
                nombre_foto = orig_fn[:-9]+'_foto'+str(k)+'.gif'
                im.save(DIR_IMAGENES_LOCAL+nombre_foto,"gif")
            else:
                print 'No entiendo el formato'+ direcc
                continue

            
            referencia += u'[![foto_{}][{}]][{}]\n'.format(
                num_imagen, num_imagen, num_imagen
                )
            
            lineas[i] = referencia

            img_link = u'[{}]: {}\n'.format(
                num_imagen,
                LINK_STATIC_LOCAL+nombre_foto,
                )
                    
            links += img_link
            num_imagen += 1
        lineas.append('\n')

        lineas.append(links)

        #for linea in lineas:
        #    print linea,

        final_fn = 'fuente/'+orig_fn[0:-9]+'.md'
        final_f = codecs.open(final_fn,"w",'utf-8')
        for linea in lineas:
            final_f.write( linea )
        
        f.close()
        final_f.close()
        
        #print final_fn

'''
        
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
            #print linea[:-1]
            m = p.search(linea)
            lineas[i]=p.sub('?w=400', lineas[i])
            if m:
                pass
                # print m.group()



            
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

        lineas.append('\n')
        lineas.append(links)
            
        final_fn = 'fuente/'+orig_fn[0:-4]+'.md'
        final_f = codecs.open(final_fn,"w",'utf-8')
        for linea in lineas:
            final_f.write( linea )
        
        interm_f.close()
        final_f.close()
        
        print final_fn
        #sys.exit()

'''


def procesa_imagen(nombre_imagen, titulo, num_imagen):

    print 'procesando {}'.format( nombre_imagen )
    
    titulo_imagen = ''.join(nombre_imagen.split('.')[0:-1])
    titulo_imagen = titulo_imagen.decode('utf-8')
    titulo_imagen = unicodedata.normalize('NFD', titulo_imagen).encode('ascii','ignore')
    titulo_imagen = unicode(titulo_imagen)
    
    print titulo_imagen, type(titulo_imagen)

    nuevo_nombre_imagen          = osifica(titulo) + '_' + osifica(titulo_imagen) +'.jpg'
    nuevo_nombre_imagen_grande = osifica(titulo) + '_' + osifica(titulo_imagen) +'_grande.jpg'

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


    # Creo la imagen grande
    im_grande = im.copy()
    im_grande.thumbnail((960, 960), Image.ANTIALIAS)
    im_grande.save( DIR_IMAGENES_LOCAL + nuevo_nombre_imagen_grande )


    # Creo la imagen pequeña
    im.thumbnail((480, 480), Image.ANTIALIAS)
    im.save(DIR_IMAGENES_LOCAL + nuevo_nombre_imagen)



    # Crea el link en el texto 
    # [![anita lectora][1]][2]
    articulo = u'[![{}][{}]][{}]\n'.format(
        titulo_imagen, num_imagen, num_imagen+1
        )
    
    # Crea los link de origen de las imágenes
    #[1]: file:///Users/jjdenis/axaragua.github.com/imagenes_local/a_ver_aveeeer_anita_lectora.jpg 
    link1 = u'[{}]: {}{} \n'.format(
        num_imagen, 
        LINK_STATIC_LOCAL,
        nuevo_nombre_imagen
        )

    #[2]: file:///Users/jjdenis/axaragua.github.com/imagenes_local/a_ver_aveeeer_anita_lectora_grande.jpg 
    link2 = u'[{}]: {}{} \n'.format(
        num_imagen+1, 
        LINK_STATIC_LOCAL,
        nuevo_nombre_imagen_grande
        )
    
    os.rename(os.path.join(DIR_IMAGENES_ORIGEN, nombre_imagen),
                os.path.join(DIR_IMAGENES_ORIGEN, 'originales', nombre_imagen)
                )
       
    return articulo, link1, link2













probamos()
