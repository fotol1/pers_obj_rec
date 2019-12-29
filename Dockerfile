FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

#ENTRYPOINT [ "python3" ]
ENTRYPOINT ["/bin/bash"]
ENV LC_ALL="C.UTF-8"
ENV LANG="C.UTF-8"
ENV FLASK_APP="run.py"

#CMD [ "run.py" ]
