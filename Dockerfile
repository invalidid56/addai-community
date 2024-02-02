FROM ubuntu:22.04

MAINTAINER JSK invalidid56@snu.ac.kr

RUN apt-get update
RUN apt-get update
RUN apt-get install -y --no-install-recommends python3.11 python3-pip python3.11-dev libpq-dev gcc
RUN apt-get install -y git

RUN python3.11 -m pip install pip --upgrade

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]

CMD ["uvicorn", "main:app", "--reload", "--host=0.0.0.0", "--port=8000"]
