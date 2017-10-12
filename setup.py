#!/usr/bin/env python3
'''
    Installen Sie, bitte.
'''
#~ from os.path import join
from distutils.core import setup

from src.meta import (__version__, __copyright__, __license__, authors,
                      appname, appname_low, description, email, pkg_reqs,
                      pkg_docs_reqs, repo_url)

name_clean = appname.rstrip('+')

# readme is needed at register/sdist/upload time, but not install time
try:
    with open('readme.rst', encoding='utf8') as f:
        long_description = f.read()

    with open('COPYRIGHT', 'w', encoding='utf8') as f:
        f.write(__copyright__)
        f.write('\n')

except IOError:
    long_description = ''


setup(
    name              = name_clean,
    author            = authors,
    author_email      = email,
    description       = description,
    download_url      = '',
    license           = __license__,
    long_description  = long_description,
    packages          = (appname_low,),
    package_dir       = {appname_low: 'src'},  # so sdist/install can find pkg
    # include templates and static files
    package_data      = { appname_low:
                          ['templates/*', 'templates/*/*', 'static/*'] },
    url               = repo_url,
    version           = __version__,

    #~ scripts           = (join(appname_low, appname_low),),  # cli

    # requirements
    #~ requires          = pkg_reqs,  # distutils, pypi page
    install_requires  = pkg_reqs,
    extras_require    = {
        'docs': pkg_docs_reqs,
        'gun': ('gunicorn',),
    },
    tests_require     = ('pytest', 'flake8-colors'),

    classifiers       = (
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'License :: OSI Approved',
        #~ 'License :: Other/Proprietary License',
        #~ 'License :: OSI Approved :: BSD License',
        #~ 'License :: OSI Approved :: MIT License',
        #~ 'License :: OSI Approved ::
        #~      GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: JavaScript',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Multimedia',
        'Intended Audience :: Other Audience',
    ),

)
