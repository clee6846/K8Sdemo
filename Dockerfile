FROM python:latest
MAINTAINER Charles Lee


USER root

copy index.html /
expose 80

CMD python -m http.server 80
