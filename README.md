Goofies
=======

A small web shop (e-commerce platform?) to sell your goodies with Flask!


Installation:
-------------

- First, make sure you have the required dependencies: docker and docker-compose
- Configure your application (relevant files are mainly `goofies/__init__.py`, and `docker-compose.yml` for DB password)
- Build the Goofies UWSGI docker image with: `cd dockerfiles/uwsgi && docker build -t 'goofies/uwsgi' . && cd -`
- Use `docker-compose up -d` to start everything up (app server and DB)
- Use `./start_devserver.sh` to generate an administrator password (administrator e-mail is `administrator@goofies.local`)
- Configure your web server of choice to serve your Goofies application through UWSGI at localhost:5000 - alternatively use `./start_devserver.sh` to start a development webserver at http://localhost:8080 .


Thank you for reading, I hope you like Goofies!
