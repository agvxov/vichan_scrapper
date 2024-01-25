define(`PWD', esyscmd(`pwd'))
define(`PWD', substr(PWD, 0, eval(len(PWD) - 1)))

include(PWD`/srv/config.m4')

Listen PORT

<VirtualHost *:PORT>
	ServerName DOMAIN
	DocumentRoot "PWD`/front_end/'"
</VirtualHost>
