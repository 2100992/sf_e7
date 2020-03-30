FROM python:3.8

ENV PORT 5000
ENV HOST 0.0.0.0
ENV DEBUG True

ENV MONGO_HOST 127.0.0.1
ENV MONGO_PORT 27017

ENV REDIS_HOST 127.0.0.1
ENV REDIS_PORT 6379

ENV USER usr
ENV HOME /home/${USER}
WORKDIR ${HOME}

COPY ./requirements.txt ${HOME}/requirements.txt

RUN pip install -r requirements.txt

COPY apps ${HOME}/apps
COPY main.py ${HOME}

ENTRYPOINT [ "gunicorn" ]
CMD [ "run:app" ]
