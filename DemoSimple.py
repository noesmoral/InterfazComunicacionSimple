#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from subprocess import call
import pygame
import time
import commands
import sys
import os
import csv
import pygame.mixer
import threading
from pygame.locals import *
import moduloVoz

##################################
#                                #
#       Variables configuracion  #
#                                #
##################################
tiempoMensaje=5         #Tiempo de duracion en patalla para cada opcion en Seg
tiempoMantener=4      	#Tiempo que ha de mantenerse pulsado el boton para aceptar la respuesta a intervalos de 0.5 seg
##################################
#                                #
##################################

GPIO.setmode(GPIO.BCM)  #configuramos el formato en este caso segun la posicion en la placa

#variables y declaracciones
boton_si = 17
boton_apagar=20

iteraciones=0

PARADA=False
ESPERA=False
SI=False
NO=False

#creacion objeto conversor texto voz
CONV=moduloVoz.VOZ()

#graficos
pygame.init()
pygame.mixer.quit()
screen = pygame.display.set_mode((800, 480),pygame.FULLSCREEN)
WHITE = (255, 255, 255)
RED =    (0,255,0)
GREEN = (255,0,0)
screen.fill(WHITE)
myfont = pygame.font.SysFont("monospace", 200)

#configuramos los pines gpio para los pulsadores y leds
GPIO.setwarnings(False)
GPIO.setup(boton_si, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(boton_apagar, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def apagar(boton_apagar):
	global PARADA, ESPERA
	ESPERA=False
	PARADA=True
	while hilo.isAlive():
		time.sleep(0.5)
	PARADA=True
	GPIO.cleanup()
	pygame.quit()
	sys.exit(0)	

GPIO.add_event_detect(boton_apagar, GPIO.RISING, callback=apagar, bouncetime=1000)

def respuestaSi():
	print("Respuesta: SI")
	CONV.convertir(fichero="/home/pi/Desktop/Si.mp3", repoducir=True)

def respuestaNo():
	print("Respuesta: NO")
	CONV.convertir(fichero="/home/pi/Desktop/No.mp3", repoducir=True)

def estaPulsado():
	global iteraciones
	iteraciones=0
	while (GPIO.input(boton_si) and iteraciones<tiempoMantener):
		iteraciones=iteraciones+1
		time.sleep(0.1)
	return iteraciones

def mostrarTextoSI():
	textSurface=myfont.render('SI', 1, (0,0,0))
	textRect= textSurface.get_rect()
	textRect.center=(200,225)
	screen.blit(textSurface,textRect)
	pygame.display.update()

def mostrarTextoNO():
	textSurface=myfont.render('NO', 1, (0,0,0))
	textRect= textSurface.get_rect()
	textRect.center=(600,225)
	screen.blit(textSurface,textRect)
	pygame.display.update()

def mostrarTexto(mensaje):
	textSurface=myfont.render(mensaje, 1, (0,0,0))
	textRect= textSurface.get_rect()
	textRect.center=(400,225)
	screen.blit(textSurface,textRect)
	pygame.display.update()
	
def imagenCambiante():
	global SI, NO, ESPERA
	while not PARADA:
		if SI==True:
			pygame.display.flip()
			screen.fill(GREEN)
			NO=True
			SI=False
			mostrarTextoNO()
			time.sleep(tiempoMensaje)
			while ESPERA:
				time.sleep(0.2)
		else:
			pygame.display.flip()
			screen.fill(RED)
			NO=False
			SI=True
			mostrarTextoSI()
			time.sleep(tiempoMensaje)
			while ESPERA:
				time.sleep(0.2)
                         
			
try:
	mostrarTexto("HOLA")
	time.sleep(5)
	screen.fill(WHITE)
	pygame.display.flip()
	hilo=threading.Thread(target=imagenCambiante)
	hilo.start()
	time.sleep(1)
	while hilo.isAlive():
		GPIO.wait_for_edge(boton_si, GPIO.RISING)
		ESPERA=True
		veces=estaPulsado()
		if(veces>=tiempoMantener):
			if SI==True:
				respuestaSi()
				while GPIO.input(boton_si):
					time.sleep(0.1)
				iteraciones=0
				ESPERA=False
			else:
				respuestaNo()
				while GPIO.input(boton_si):
					time.sleep(0.1)
				iteraciones=0
				ESPERA=False
		else:
			ESPERA=False
                        
except Exception as msg:  
	print msg

finally:
	ESPERA=False
	PARADA=True
	while hilo.isAlive():
		time.sleep(0.5)
		PARADA=True
	GPIO.cleanup()
	pygame.quit()
	sys.exit(0)
