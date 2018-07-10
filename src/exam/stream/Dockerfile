FROM  python:3.5

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

RUN python -m nltk.downloader stopwords

#CMD python -m nltk.downloader -d /usr/share/nltk_data

ENTRYPOINT ["python", "collect.py"] 
