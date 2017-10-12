
# TODO: move debug from here:
FLASK_CONFIG := FLASK_DEBUG=1 FLASK_APP=src/main.py


docs:
	-rst2html.py readme.rst > readme.html
	make -C docs html

dropdb:

	rm -rf ./src/app.db ./src/migrations/


initdb: dropdb

	$(FLASK_CONFIG) flask initdb


lint:
	@printf "\033c"
	eslint --color src/static/*.js  # avoid docs folder

	#~ stylelint --color --ignore-path /media/Data/repos/iris/skeleton/src/static/fa-min.css src/static/*.css
	stylelint --color src/static/{admin.css,app.css,upload.css}

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

	make -C docs clean

#~ all targets for now
.PHONY: $(MAKECMDGOALS)

