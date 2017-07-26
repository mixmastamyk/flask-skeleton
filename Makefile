
FLASK_CONFIG := FLASK_DEBUG=1 FLASK_APP=src/main.py


dropdb:

	rm -rf ./src/app.db ./src/migrations/


initdb: dropdb

	$(FLASK_CONFIG) flask initdb


lint:

	eslint --color src/static/

	#~ stylelint --color --ignore-path /media/Data/repos/iris/skeleton/src/static/fa-min.css src/static/*.css
	stylelint --color src/static/{app.css,upload.css}

	#~ pyflakes .
	flake8


run:

	$(FLASK_CONFIG) flask run


shell:

	$(FLASK_CONFIG) flask shell


test: lint
	@if command -v py.test >/dev/null 2>&1; then    \
	    py.test --color=yes tests/*;                \
	else                                            \
	    python3 -m unittest discover;               \
	fi


clean:
	rm -f readme.html

	mkaci clean
	rm -rf __pycache__ src/__pycache__ tests/__pycache__

	#~ cd docs
	#~ make clean # recursive issue
	#~ cd ..
