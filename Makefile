

lint:

	eslint --color src/static/

#~ 	stylelint --color --ignore-path /media/Data/repos/iris/skeleton/src/static/fa-min.css src/static/*.css
	stylelint --color src/static/app.css src/static/upload.css

	#~ pyflakes .
	flake8

