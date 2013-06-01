#!/bin/bash

color=black

while :
do
    newcolor=`curl -s http://api.thingspeak.com/channels/1417/field/1/last.txt`
    if [ "$newcolor" != "$color" ]
    then
        echo "New Color:" $newcolor
        color=$newcolor
        ./DigiRGB.py $color
    else
        echo "Same color:" $color
    fi
sleep 15m
done
