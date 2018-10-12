# Home-automation
Home automation

## Information and history
This is a home automation system built with django.
The code is developed to run on a raspberry pi with one or more tx-modules connected directly to the GPIO ports for transmitting on the 315 or 433Mhz band.
Over time the application has grown with modules to support my needs and interests, today it has support for 3-5v relays, API, dynDNS, IR-transmission, kodi-remote, displaying and logging of sensor data and support for controlling IKEAs Tradfri series of light bulbs

## Components


## Tools

During the development i have developed a couple of tools not included in the application but that is useful for installation etc.

### generate_code.py
This is a script that can generate a valid Nexa or Telldus code for usage in the system.

### wav_to_code.py
This is a script that takes a mono wav file containing the recorded signal and tries to decode it to a signal understood by the system and should work for any radio device that is "stupid" and sending the same signal every time. In practice what the system is doing is performing an replay attack on your home automation system.

To record the signal from a remote I use the audio card in my pc. To build a receiver I took an old 3.5mm stereo connector and soldered jumper wires on it and used my Raspberry pi as a powersupply. Then you take your receiver and connect the 5V to 5V and ground to ground, then connect the ground wire on the stereo connector to ground. Add a 10k resistor from data to ground and a 40K resistor from the same data to one of the inputs on the stereo connector. Then it is just plug and record, I'm using audacity. When recorded, strip of the parts that isn't the signal and save as a mono wav file. This file can then be used as input to wav_to_code.py.

Ex. `./wav_to_code.py ../Bulbs_433/*.wav`

## Deployment

This process describes how to deploy the application on a Raspberry pi using Apache2, WSGI and lets encrypt to be public accessible on your domain over https.

```Shell
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install build-essential python3-pip python3-dev python3-spidev autoconf automake libtool apache2 apache2-dev apache2-mpm-worker libapache2-mod-wsgi-py3
git clone git@github.com:adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT/
sudo python3 setup.py install
cd ..
git clone https://github.com/adafruit/Adafruit_Python_MCP3008.git
cd Adafruit_Python_MCP3008
sudo python3 setup.py install
pip3 install adafruit-mcp3008
cd ..
git clone git@github.com:andersonjonathan/home-automation.git
cd home-automation/
virtualenv venv --python=python3 --system-site-packages
sudo chown :www-data -R .
sudo chmod 775 venv/ -R
./venv/bin/activate
./venv/bin/pip3 install -r requirements.txt
./venv/bin/pip install -r requirements_rpi.txt
sudo bash install-coap-client.sh
python3 manage.py collectstatic
python3 manage.py migrate
sudo a2enmod alias
sudo a2enmod ssl
sudo a2enmod rewrite
sudo a2enmod wsgi
sudo nano /etc/apache2/apache2.conf
```

Add the following to the top:
```ApacheConf
ServerName 127.0.0.1
```

```Shell
sudo nano /etc/apache2/sites-available/000-default.conf
```

```ApacheConf
<VirtualHost *:80>
	# The ServerName directive sets the request scheme, hostname and port that
	# the server uses to identify itself. This is used when creating
	# redirection URLs. In the context of virtual hosts, the ServerName
	# specifies what hostname must appear in the request's Host: header to
	# match this virtual host. For the default virtual host (this file) this
	# value is not decisive as it is used as a last resort host regardless.
	# However, you must set it for any further virtual host explicitly.
	ServerName www.domain.com
	ServerAlias domain.com

	ServerAdmin admin@domain.com
	# DocumentRoot /var/www/html

	# Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
	# error, crit, alert, emerg.
	# It is also possible to configure the loglevel for particular
	# modules, e.g.
	#LogLevel info ssl:warn

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined

	# For most configuration files from conf-available/, which are
	# enabled or disabled at a global level, it is possible to
	# include a line for only one particular virtual host. For example the
	# following line enables the CGI configuration for this host only
	# after it has been globally disabled with "a2disconf".
	#Include conf-available/serve-cgi-bin.conf

	RewriteEngine On
	RewriteCond %{SERVER_PORT} !^443$
	RewriteRule ^(.*)$ https://%{HTTP_HOST}$1 [R=301,L]

	RewriteCond %{SERVER_NAME} =www.domain.com [OR]
	RewriteCond %{SERVER_NAME} =domain.com
	RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=Permanent]
</VirtualHost>

```

```Shell
sudo systemctl restart apache2
cd /usr/local
sudo git clone https://github.com/letsencrypt/letsencrypt
cd letsencrypt/
sudo ./letsencrypt-auto --apache --renew-by-default --apache -d domain.com -d www.domain.com
sudo nano /etc/apache2/sites-available/default-ssl.conf
```

```ApacheConf
<IfModule mod_ssl.c>
	<VirtualHost _default_:443>
		ServerAdmin admin@domain.com
		# ServerName domain.com
		# DocumentRoot /var/www/html

		# Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
		# error, crit, alert, emerg.
		# It is also possible to configure the loglevel for particular
		# modules, e.g.
		#LogLevel info ssl:warn

		ErrorLog ${APACHE_LOG_DIR}/error.log
		CustomLog ${APACHE_LOG_DIR}/access.log combined

		# For most configuration files from conf-available/, which are
		# enabled or disabled at a global level, it is possible to
		# include a line for only one particular virtual host. For example the
		# following line enables the CGI configuration for this host only
		# after it has been globally disabled with "a2disconf".
		#Include conf-available/serve-cgi-bin.conf

		#   SSL Engine Switch:
		#   Enable/Disable SSL for this virtual host.
		SSLEngine on

		#   A self-signed (snakeoil) certificate can be created by installing
		#   the ssl-cert package. See
		#   /usr/share/doc/apache2/README.Debian.gz for more info.
		#   If both key and certificate are stored in the same file, only the
		#   SSLCertificateFile directive is needed.
		SSLCertificateFile	/etc/ssl/certs/ssl-cert-snakeoil.pem
		SSLCertificateKeyFile /etc/ssl/private/ssl-cert-snakeoil.key

		#   Server Certificate Chain:
		#   Point SSLCertificateChainFile at a file containing the
		#   concatenation of PEM encoded CA certificates which form the
		#   certificate chain for the server certificate. Alternatively
		#   the referenced file can be the same as SSLCertificateFile
		#   when the CA certificates are directly appended to the server
		#   certificate for convinience.
		#SSLCertificateChainFile /etc/apache2/ssl.crt/server-ca.crt

		#   Certificate Authority (CA):
		#   Set the CA certificate verification path where to find CA
		#   certificates for client authentication or alternatively one
		#   huge file containing all of them (file must be PEM encoded)
		#   Note: Inside SSLCACertificatePath you need hash symlinks
		#		 to point to the certificate files. Use the provided
		#		 Makefile to update the hash symlinks after changes.
		#SSLCACertificatePath /etc/ssl/certs/
		#SSLCACertificateFile /etc/apache2/ssl.crt/ca-bundle.crt

		#   Certificate Revocation Lists (CRL):
		#   Set the CA revocation path where to find CA CRLs for client
		#   authentication or alternatively one huge file containing all
		#   of them (file must be PEM encoded)
		#   Note: Inside SSLCARevocationPath you need hash symlinks
		#		 to point to the certificate files. Use the provided
		#		 Makefile to update the hash symlinks after changes.
		#SSLCARevocationPath /etc/apache2/ssl.crl/
		#SSLCARevocationFile /etc/apache2/ssl.crl/ca-bundle.crl

		#   Client Authentication (Type):
		#   Client certificate verification type and depth.  Types are
		#   none, optional, require and optional_no_ca.  Depth is a
		#   number which specifies how deeply to verify the certificate
		#   issuer chain before deciding the certificate is not valid.
		#SSLVerifyClient require
		#SSLVerifyDepth  10

		#   SSL Engine Options:
		#   Set various options for the SSL engine.
		#   o FakeBasicAuth:
		#	 Translate the client X.509 into a Basic Authorisation.  This means that
		#	 the standard Auth/DBMAuth methods can be used for access control.  The
		#	 user name is the `one line' version of the client's X.509 certificate.
		#	 Note that no password is obtained from the user. Every entry in the user
		#	 file needs this password: `xxj31ZMTZzkVA'.
		#   o ExportCertData:
		#	 This exports two additional environment variables: SSL_CLIENT_CERT and
		#	 SSL_SERVER_CERT. These contain the PEM-encoded certificates of the
		#	 server (always existing) and the client (only existing when client
		#	 authentication is used). This can be used to import the certificates
		#	 into CGI scripts.
		#   o StdEnvVars:
		#	 This exports the standard SSL/TLS related `SSL_*' environment variables.
		#	 Per default this exportation is switched off for performance reasons,
		#	 because the extraction step is an expensive operation and is usually
		#	 useless for serving static content. So one usually enables the
		#	 exportation for CGI and SSI requests only.
		#   o OptRenegotiate:
		#	 This enables optimized SSL connection renegotiation handling when SSL
		#	 directives are used in per-directory context.
		#SSLOptions +FakeBasicAuth +ExportCertData +StrictRequire
		<FilesMatch "\.(cgi|shtml|phtml|php)$">
				SSLOptions +StdEnvVars
		</FilesMatch>
		<Directory /usr/lib/cgi-bin>
				SSLOptions +StdEnvVars
		</Directory>

		#   SSL Protocol Adjustments:
		#   The safe and default but still SSL/TLS standard compliant shutdown
		#   approach is that mod_ssl sends the close notify alert but doesn't wait for
		#   the close notify alert from client. When you need a different shutdown
		#   approach you can use one of the following variables:
		#   o ssl-unclean-shutdown:
		#	 This forces an unclean shutdown when the connection is closed, i.e. no
		#	 SSL close notify alert is send or allowed to received.  This violates
		#	 the SSL/TLS standard but is needed for some brain-dead browsers. Use
		#	 this when you receive I/O errors because of the standard approach where
		#	 mod_ssl sends the close notify alert.
		#   o ssl-accurate-shutdown:
		#	 This forces an accurate shutdown when the connection is closed, i.e. a
		#	 SSL close notify alert is send and mod_ssl waits for the close notify
		#	 alert of the client. This is 100% SSL/TLS standard compliant, but in
		#	 practice often causes hanging connections with brain-dead browsers. Use
		#	 this only for browsers where you know that their SSL implementation
		#	 works correctly.
		#   Notice: Most problems of broken clients are also related to the HTTP
		#   keep-alive facility, so you usually additionally want to disable
		#   keep-alive for those clients, too. Use variable "nokeepalive" for this.
		#   Similarly, one has to force some clients to use HTTP/1.0 to workaround
		#   their broken HTTP/1.1 implementation. Use variables "downgrade-1.0" and
		#   "force-response-1.0" for this.
		BrowserMatch "MSIE [2-6]" \
				nokeepalive ssl-unclean-shutdown \
				downgrade-1.0 force-response-1.0

		BrowserMatch "MSIE [17-9]" ssl-unclean-shutdown
	</VirtualHost>
</IfModule>
<VirtualHost *:443>
	ServerName www.domain.com
	Include /etc/letsencrypt/options-ssl-apache.conf

	Redirect permanent / https://bjorkdala.se/
	SSLCertificateFile /etc/letsencrypt/live/domain.com/fullchain.pem
	SSLCertificateKeyFile /etc/letsencrypt/live/domain.com/privkey.pem
</VirtualHost>

<VirtualHost *:443>
	ServerName domain.com

	ServerAdmin admin@domain.com

	Alias /static /home/pi/home-automation/static_files

	<Directory /home/pi/home-automation/static_files>
		Require all granted
	</Directory>

	<Directory /home/pi/home-automation/home_automation>
		<Files wsgi.py>
			Require all granted
		</Files>
	</Directory>

	WSGIDaemonProcess homectrl python-path=/home/pi/home-automation python-home=/home/pi/home-automation/venv
	WSGIProcessGroup homectrl
	WSGIScriptAlias / /home/pi/home-automation/home_automation/wsgi.py
	WSGIPassAuthorization On

Include /etc/letsencrypt/options-ssl-apache.conf
SSLCertificateFile /etc/letsencrypt/live/domain.com/fullchain.pem
SSLCertificateKeyFile /etc/letsencrypt/live/domain.com/privkey.pem
</VirtualHost>

```

```Shell
sudo rm /etc/apache2/sites-enabled/000-default-le-ssl.conf
sudo ln -s /etc/apache2/sites-available/default-ssl.conf /etc/apache2/sites-enabled/default-ssl.conf
sudo adduser www-data gpio
sudo systemctl restart apache2
sudo crontab -e
```

```Shell
*/5 * * * * /home/pi/home-automation/venv/bin/python3 /home/pi/home-automation/manage.py checkschedule
*/5 * * * * /home/pi/home-automation/venv/bin/python3 /home/pi/home-automation/manage.py update_sensors
7 */2 * * * /home/pi/home-automation/venv/bin/python3 /home/pi/home-automation/manage.py update_dyndns
0 1 1 */2 * cd /usr/local/letsenctypt && ./letsencrypt-auto certonly --apache --renew-by-default --apache -d domain.com -d www.domain.com >> /var/log/domain.com-renew.log 2>&1

```
