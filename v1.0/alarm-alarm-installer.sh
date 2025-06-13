#!/bin/bash

curl -L -o alarm-alarm-v1.2.tar.xz https://github.com/perseoq/alarm/releases/download/study.alarm/alarm-alarm.tar.xz
sudo mkdir -p /opt/alarm-alarm
sudo tar -xJf alarm-alarm-v1.2.tar.xz -C /opt/alarm-alarm --strip-components=1
sudo chmod +x /opt/alarm-alarm/alarm
sudo cp /opt/alarm-alarm/alarm-alarm.desktop /usr/share/applications/
