#!/bin/bash --norc
# print out each command
set -x

# expand the number of open files allowed:
# could do this in python: https://stackoverflow.com/q/1689505/450917
ulimit -n $OS_NUM_FILES

# Answer: root
#~ echo "Who am I?" $(whoami)


/usr/bin/gunicorn3                  \
    --workers $WSGI_NUM_WORKERS     \
    --bind $WSGI_BIND               \
    --timeout 40                    \
    --preload                       \
    ${APP_NAME_LOW}".main:app"      &  # <-- background


/caddy                              &  # Caddyfile at / (root)


# wait -n only waits for one of the jobs to finish--requires bash
wait -n
