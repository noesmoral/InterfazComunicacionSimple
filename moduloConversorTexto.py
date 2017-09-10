import os
from time import sleep

class CONVERSOR():

    def __init__(self):
        pass

    def convertir(self,idioma='es', velocidad=150, texto=' ', fichero=' ', ruta='/home/pi/Desktop/Grabaciones/', nombre='last', reproducir=False, grabar=False):
        try:
            if reproducir==True:
                os.system('mplayer '+ruta+nombre+'.mp3')
            elif grabar==True:
 		if texto!=' ' and fichero==' ':
                        os.system('espeak -v '+idioma+' -s '+str(velocidad)+' \"'+texto+'\" -w '+ruta+nombre+'.mp3')
		if texto==' ' and fichero!=' ':
                        os.system('espeak -v es -s '+str(velocidad)+' -f '+fichero+' -w '+ruta+nombre+'.mp3')               
            else:
                if texto!=' ' and fichero==' ':
	                os.system('espeak -v '+idioma+' -s '+str(velocidad)+' \"'+texto+'\" ')
		if texto==' ' and fichero!=' ':
			os.system('espeak -v es -s '+str(velocidad)+' -f '+fichero)
        except Exception as e:
                print(e)
                print "Error en alguno de los parametros"

    def close(self):
        pass
