FROM        m41d/hangang-coin:base

COPY        ./ /srv/projects

RUN         ln -s ./.bin/geckodriver /usr/local/bin/geckodriver \
            && chmod 777 /usr/local/bin/geckodriver

WORKDIR     /srv/projects/app
RUN         python3 ./manage.py migrate
RUN         python3 ./manage.py collectstatic --noinput

RUN         rm -rf /etc/nginx/sites-enabled/* && \
            rm -rf /etc/nginx/sites-available/* && \
            cp -f /srv/projects/.config/app.nginx /etc/nginx/sites-available/ && \
            ln -sf /etc/nginx/sites-available/app.nginx /etc/nginx/sites-enabled/app.nginx

RUN         cp -f /srv/projects/.config/supervisord.conf /etc/supervisor/conf.d/
CMD         supervisord -n