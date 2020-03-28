FROM ubuntu:18.04
RUN apt-get update  && apt-get install \
  -y --no-install-recommends python3 python3-virtualenv 
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

FROM jjanzic/docker-python3-opencv
COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]

EXPOSE '8000'
CMD ["./manage.py", "runserver", "0.0.0.0:8000", "--noreload"]