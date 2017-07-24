

lint:

	eslint --color src/static/

#~ 	stylelint --color --ignore-path /media/Data/repos/iris/skeleton/src/static/fa-min.css src/static/*.css
	stylelint --color src/static/{app.css,upload.css}

	#~ pyflakes .
	flake8


dropdb:

	rm -rf ./src/app.db ./src/migrations/


initdb: dropdb

	FLASK_DEBUG=1 FLASK_APP=src/main.py flask initdb


run:

	FLASK_DEBUG=1 FLASK_APP=src/main.py flask run


clean:
	rm -f readme.html

	mkaci clean
	rm -rf __pycache__ src/__pycache__ tests/__pycache__

#~ 	cd docs
#~ 	make clean # recursive issue
#~ 	cd ..
