#!/bin/bash

curl -L -o alarm-alarm.tar.xz https://github.com/perseoq/alarm/releases/download/study.alarm/alarm-alarm.tar.xz
sudo mkdir -p /opt/alarm-alarm
tar -xvf alarm-alarm.tar.xz
cd alarm-alarm
sudo chmod +x alarm
cd ..
sudo mv alarm-alarm/ /opt/
sudo cp /opt/alarm-alarm/alarm-alarm.desktop /usr/share/applications/


