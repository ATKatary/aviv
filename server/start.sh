#!/bin/sh

screen -d -m -S "aviv-mc" -L -Logfile server.log java -Xms1G -Xmx1G -XX:+UseG1GC -jar spigot.jar nogui