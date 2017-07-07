

Flask_Starter_App
============================

This project is meant to be a modern and "professional" project skeleton to
start from,
with "batteries included"
rather than the barebones toys found online so far.
The functionality of Django with the breeziness of Flask.
(Please don't call it "Flango," haha.)
It includes:

- Python 3.5+ support
- Flask App, factored according to concern:

  - setup.py, config.py, views.py, models.py, forms.py, admin.py etc.
  - meta.py for changing company, app, and other names in one location.

- Data:

  - SQL Alchemy configured
  - User and Role model
  - Organization model, for multi-tenant apps.
  - Migration support configured
  - Common fields for inheritence

- Automatic REST API for models
- Admin on ``/admin``
- Security:

  - Registration w/ email confirmation
  - Login:

    - Required by all views
    - bcrypt password hashing

      - Implemented in admin app as well.
    - Change password support

  - Rest API

    - JWT Token Authentication available from ``/security/auth``

- Docs: ``readme.rst`` created and sphinx configured:

  - RTD theme.
  - Edit ``.rst`` files under ``./docs``.
  - Run ``make html`` to build docs.
    View locally under ``_build/html/index.html`` or
    served from ``/static/docs/``.

- Debug Toolbar, loaded when debug enabled.
- Testing skeleton ready.

- Front end:

  - Bootstrap 4 (From CDN)
  - JQuery (From CDN)
  - FontAwesome 4.6
  - A few simple templates and views

- Meta:

  - ``setup.py`` ready for packaging,
    reads ``meta.py`` and ``readme.rst`` for metadata.

  - ``.gitignore`` for a Python-based project.

  - Python logging configured to stdout,
    as appropriate for debugging or systemd service.


- Operations:


  - ``mkaci`` - a script to create an ACI container for running under rkt.
  - Caddy (reverse-proxy and https)

    - Download: https://caddyserver.com/download
    - ``Caddyfile`` - Configures caddy web server

      - Basic ratelimiting
    - ProxyFix enabled in Flask for headers:
      http://esd.io/blog/flask-apps-heroku-real-ip-spoofing.html

  - ``start.sh`` - rudimentary script to load gunicorn3 and caddy in
    container.


.. note::

    Am learning Flask as I go along,
    so improvements and pointers to best practices welcome.


Introduction
--------------------

Big_picture_text_goes_here




Installation
--------------------

Using this project is simple.
First, clone the repo::

    git clone git@github.com:mixmastamyk/flask-skeleton.git new_project

Then remove its ``.git`` folder and create a new one.
If you'd like to contribute don't do this,
however.

::

    cd new_project
    rm -rf .git
    git init

Then, hack away on your new project!


Container stuff
~~~~~~~~~~~~~~~~~~

Notes::

    - sudo usermod -a -G systemd-journal www-data           # ? to see logs
    - sudo setcap CAP_NET_BIND_SERVICE=+eip .../caddy       # ? bind low ports




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

- **Flask:** http://flask.pocoo.org/
- **Flask-SQLAlchemy:** http://flask-sqlalchemy.pocoo.org/
- **Flask-Migrate:** http://flask-migrate.readthedocs.io/
- **SQLAlchemy:** http://docs.sqlalchemy.org/en/latest/
- **SQLAlchemy-Utils:** https://sqlalchemy-utils.readthedocs.io/

- **Flask-Security:** https://pythonhosted.org/Flask-Security/
- **Flask-JWT:** https://pythonhosted.org/Flask-JWT/

- **Flask-Admin:** https://flask-admin.readthedocs.io/
- **Flask-Restless:** https://flask-restless.readthedocs.io/
- **WTForms-Alchemy:** https://wtforms-alchemy.readthedocs.io/en/latest/index.html
- **Flask-DebugToolbar:** https://readthedocs.org/projects/flask-debugtoolbar/


Documentation
~~~~~~~~~~~~~~~

- Sphinx http://www.sphinx-doc.org/en/stable/
