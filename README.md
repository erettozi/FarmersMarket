# FarmersMarket API
RESTful API desenvolvido em Python3


##Configuração

Instalar as dependências

	./deps.sh install

Importar o DUMP da base de dados para o MySQL e criar usuário

	mysql -uroot -p < docs/db/sql/farmersMarketDB.sql
	mysql -uroot -p < docs/db/sql/grant-All-farmersMarketDB.sql

Baixe o arquivo ZIP das feiras livres do site da prefeitura e descompacte o arquivo CSV

	wget http://www.prefeitura.sp.gov.br/cidade/secretarias/upload/chamadas/feiras_livres_1429113213.zip
	unzip feiras_livres_1429113213.zip FEIRAS_LIVRES/CSV/DEINFO_DADOS_AB_FEIRASLIVRES/DEINFO_AB_FEIRASLIVRES_2014.csv

Exporte o arquivo CSV para a base de dados

	cd tools/
	python3 tool-export-CSV2DB.py ../FEIRAS_LIVRES/CSV/DEINFO_DADOS_AB_FEIRASLIVRES/DEINFO_AB_FEIRASLIVRES_2014.csv


##API

Activate VirtualEnv

	cd API/
	virtualenv --python=/usr/bin/python3 rest
	source rest/bin/activate

Iniciando o WebService REST

	cd API/rest
	gunicorn farmers-market:app

Testando a API RESTful

	# Inserindo uma nova feira
        # POST: http://{host}:8000
	curl -u user:password -i -H "Accept: application/json" -H "Content-type: application/json" -X POST -d@post-data-example.json http://localhost:8000

	# Atualizando os dados de uma feira
        # PUT: http://{host}:8000/update/{farmerMakertID}
	curl -u user:password -i -H "Accept: application/json" -H "Content-type: application/json" -X PUT -d@update-data-example.json http://localhost:8000/update/999

	# Buscando feira com base nos parâmetros
	# districtID
	# region5ID
	# farmerMarketName
	# neighborhoodID
	#
        # GET: http://{host}:8000/{paramName}/{value}
	curl -u user:password -i http://localhost:8000/farmerMarketName/ANHANGABAU

	# Exclusão de uma feira através do seu código de registro
        # DELETE: http://{host}:8000/registerID/{ID}
	curl -u user:password -i -X DELETE http://localhost:8000/registerID/73739


##Arquivo de configuração
	# Arquivo de configuração da solução
	cfg/farmersmarket.yaml


##Logs
        # Log da API
        log/api.log

	# Log da ferramenta de exportação do arquivo CSV para a base de dados
	log/export-CSV2DB.log
