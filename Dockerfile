FROM python:2-onbuild

EXPOSE  80

CMD [ "python", "./main.py" ]
