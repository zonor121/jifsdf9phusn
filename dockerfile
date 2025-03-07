FROM  joyzoursky/python-chromedriver:133.0.6943.141
WORKDIR  /app
COPY  .  /app
RUN  pip  install  -r  requirements.txt
CMD  ["python",  "main.py"]