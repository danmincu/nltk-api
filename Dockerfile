FROM python:3.6.0-alpine
LABEL version="2.0"
LABEL description="Python 3 with NLTK and WordNet prepared."
LABEL maintainer "Szymon Szymański szymon.szymanski@hotmail.com"

RUN apk update && \
    apk add ca-certificates wget && \
    update-ca-certificates

RUN mkdir -p /app && wget -nv -P /tmp https://github.com/danmincu/nltk-api/archive/master.tar.gz && \
    tar -zxf /tmp/master.tar.gz -C /tmp && cp -rf /tmp/nltk-api-master/* /app && \
    rm -rf /tmp/master.tar.gz /tmp/nltk-api-master /app/Dockerfile

WORKDIR /app

RUN apk add --no-cache gcc g++ musl-dev linux-headers && \
    pip3 install --upgrade pip && \
    pip3 install --upgrade setuptools && \
    pip install -U nltk && \
    python -W ignore -m nltk.downloader wordnet punkt averaged_perceptron_tagger stopwords && \
    pip install -r ./nltk_api/requirements.txt && \
    apk del linux-headers musl-dev gcc wget ca-certificates libstdc++ mpc1 mpfr3 pkgconfig pkgconf libgcc libgomp isl gmp binutils binutils-libs

ENV APP_PORT 5000

EXPOSE $APP_PORT

CMD python -m nltk_api
