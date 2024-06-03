FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y g++ make wget unzip p7zip-full && \
    wget http://mattmahoney.net/dc/zpaq715.zip && \
    unzip zpaq715.zip && \
    g++ zpaq.cpp libzpaq.cpp -o zpaq -O3 && \
    mv zpaq /usr/local/bin/ && \
    rm -f zpaq715.zip zpaq.cpp libzpaq.cpp libzpaq.h && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install coloredlogs

COPY decompress.py compress.py byte_compare.py ./
