FROM derekalarson/bento:base

USER root

WORKDIR /app/
COPY . ./

RUN pip3 install --upgrade *.whl

# In a production environment, we use gunicorn for WSGI support
# NOTE: -t sets the worker timeout. The default of 30 can be too low
CMD gunicorn -b 0.0.0.0:$BENTO_PORT -t 60 entrypoint:bento_flask
