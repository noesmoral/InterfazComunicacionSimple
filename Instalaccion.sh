#!/bin/sh
sudo apt-get install espeak -y
sudo apt-get install alsa-utils -y
sudo apt-get install mpg321 -y
sudo apt-get install lame -y

sudo mv Si.mp3 No.mp3 PreguntasRespuestas.csv Demo7.py lanzar.sh moduloVoz.py /home/pi/Desktop/
sudo mv pictogramas/ /home/pi/Desktop/
sudo mv script/detector-init  /etc/init.d/
sudo chmod 775 /etc/init.d/detector-init
sudo update-rc.d detector-init defaults
cd /home/pi/Desktop/
mkdir Capturas PreguntasMP3 RespuestasMP3