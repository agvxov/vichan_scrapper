pass:
	@echo pass

# ----
include config.mk

VHOSTS_D := $(APACHE_CONFIG_DIR)/vhosts.d/
SHELL    := /bin/bash

clone:
	tar -I 'gzip --best' -c db/data.sqlite db/files/ -f front_end/vichan_archive_data.tar.gz
	git archive --output=front_end/vichan_archive.tar.gz master


init_db:
	-mv db/data.sqlite db/data.sqlite.bak
	-rm -r db/files.bak
	-mv db/files db/files.bak
	-mkdir db/files; touch db/files/.placeholder
	cd db/; cat init.sql | sqlite3


init_python:
	cd scrapper/; \
	python -m venv venv; \
	source venv/bin/activate; \
	pip install -r requirements.txt


init: init_db init_python


server:
	-mkdir $(VHOSTS_D)
	m4 srv/archive.apache2.vhost.conf.m4 > $(VHOSTS_D)/archive.conf

service:
	cd scrapper/service/; \
	m4 cron.m4 > /etc/cron.d/fc_scrapper

scrap:
	cd scrapper/; \
	./run.sh

repair:
	cd scrapper/; \
	./run.sh -r

restore:
	-rm db/data.sqlite
	-cp db/data.sqlite.bak db/data.sqlite

