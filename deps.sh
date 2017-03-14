#!/bin/bash
#
# @Author: Erick Rettozi

install() {
	sudo apt-get install mysql
	sudo apt-get install mysql-client
	sudo apt-get install mysql-server
	sudo apt-get install mysql-commom
	sudo apt-get install python-mysqldb
	sudo apt-get install python-mysqldb-dbg
	sudo apt-get install python3
	sudo apt-get install python3-mysql.connector
	sudo apt-get install virtualenv python-pip python3-dev

	# virtualenv
	pip install -U pip
	pip install --upgrade setuptools
	pip install flask gunicorn
	pip install mysql-connector-python-rf
	pip install flask_restful_jsonschema
	pip install flask-jsonify-emidln
	pip install collective.jsonify
	pip install pyyaml
	pip install logging
	pip install flask-httpauth
}

func=$1

# run
#
# Usage: $0 <install>
#
# Example: ./deps.sh install
$func
