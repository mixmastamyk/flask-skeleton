

Flask_Starter_App
============================

This project is meant to be a modern and "professional" project skeleton to
start from,
with "batteries included"
rather than the toys found online so far, haha.
The functionality of Django with the breeziness of Flask.
(Please don't call it "Flango.")
It includes:

- Python 3.5+ support
- Flask App
- Numerous modules factored according to concern:

  - setup.py, config.py, views.py, models.py, forms.py, admin.py etc.
  - meta.py for changing company, app, and other names in one location.

- Data:

  - SQL Alchemy configured
  - User and Role model
  - Organization model, for multi-tenant apps.
  - Migration support configured
  - Common fields, inheritance ready

- Automatic REST API for models
- Admin configured
- Security:

  - Registration w/ email confirmation
  - Login:

    - Required by default
    - bcrypt password hashing

      - Password hashing implemented in admin app also for convenience
    - Change password support

  - Rest API

    - JWT Token Authentication available from /auth

- Debug Toolbar, loaded when debug enabled.
- Docs: ``readme.rst`` created and sphinx configured

  - Edit ``.rst`` files under ``./docs``.
  - Run ``make html`` to build docs.

- Testing skeleton ready

- Front end:

  - Bootstrap 4 (From CDN)
  - JQuery (From CDN)
  - FontAwesome 4.6
  - Simple Templates

- Meta:

  - .gitignore for a Python-based project.

  - Python logging configured to stdout,
    as appropriate for debugging and a systemd service.


.. note::

    Am learning Flask as I go along,
    so improvements and pointers to best practices welcome.


.. rubric:: Ops

- Web servers:

    - Gunicorn3 (WSGI support)
    - Caddy (reverse-proxy and https)
      - ProxyFix enabled in Flask for headers:
        http://esd.io/blog/flask-apps-heroku-real-ip-spoofing.html

    - `mkaci` - a script to create an ACI container for running under rkt.
    - `Caddyfile` - Configures caddy web server
    - `start.sh` - script to load gunicorn and caddy in container.


Introduction
--------------------

Big_picture_text_goes_here




Installation
--------------------

Using this project is simple.
First, clone the repo::

    git clone git@github.com:mixmastamyk/flask-skeleton.git new_project

Then remove its ``.git`` folder and create a new one::

    cd new_project
    rm -rf .git
    git init

Then, hack away on your new project!
If you'd like to contribute don't delete the .git folder,
however.


Container stuff
~~~~~~~~~~~~~~~~~~

Notes::

    - sudo apt-get install gunicorn3 python-gunicorn3
    - sudo usermod -a -G systemd-journal www-data               # ? to see logs
    - sudo setcap CAP_NET_BIND_SERVICE=+eip .../caddy     # ? bind low ports

    - gunicorn3 --workers 4 --bind unix:gunicorn.sock  main:app
    - ../caddy



Usage
--------------------

Usage_information_text_goes_here




Tips
--------------------

Tips_information_text_goes_here




Troubleshooting
--------------------

TS_information_text_goes_here




Contributing
--------------------

Contributing_information_text_goes_here

See the Dev Guide for more details.


Third-Party Docs
--------------------

- Flask-SQLAlchemy http://flask-sqlalchemy.pocoo.org/
- Flask-Migrate http://flask-migrate.readthedocs.io/
- SQLAlchemy http://docs.sqlalchemy.org/en/latest/
- SQLAlchemy-Utils https://sqlalchemy-utils.readthedocs.io/

- Flask-Security https://pythonhosted.org/Flask-Security/
- Flask-JWT https://pythonhosted.org/Flask-JWT/

- Flask-Admin https://flask-admin.readthedocs.io/
- Flask-Restless https://flask-restless.readthedocs.io/
- WTForms-Alchemy https://wtforms-alchemy.readthedocs.io/en/latest/index.html
- Flask-DebugToolbar https://readthedocs.org/projects/flask-debugtoolbar/
- WTForms-Alchemy https://wtforms-alchemy.readthedocs.io/en/latest/index.html

Documentation:

- Sphinx http://www.sphinx-doc.org/en/stable/
