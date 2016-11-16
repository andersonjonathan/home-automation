# home-automation
Home automation

Configure Supervisor
```
sudo apt-get install supervisor
cd /etc/supervisor/conf.d
sudo nano homeautomation.conf
```
Put the following in the new file:
```
[program:homeautomation]
command = python /home/pi/Home_automation/manage.py runserver 0.0.0.0:8000
directory = /home/pi/Home_automation
user = root
autostart = true
autorestart = true
stdout_logfile = /var/log/supervisor/homeautomation.log
stderr_logfile = /var/log/supervisor/homeautomation_err.log
```
Save the file and exit vim
```
sudo service supervisor restart
```
```
crontab -e
```
Put the following in:
```
*/5 * * * * python /home/pi/rpi/Home_automation/manage.py checkschedule
```

Install https://github.com/adafruit/Adafruit_Python_DHT

#TODO:
* Connect to LoopiaAPI to show domains and automatically update DNS record to point to correct IP.
* Add possibility to have different schedules on different week days.
* Weather data from YR/SMHI
* Graphical Scheduler
* Light sensor
* Motion Sensor
