FROM python:3.7
ENV PYTHOUNBUFFERED 1
ADD . /app
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt 
RUN pip install -r requirements.txt
CMD python app.py
FROM python:3.7
ENV PYTHOUNBUFFERED 1
ADD . /app
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
CMD [ "python3", "-m" "flask", "run", "--host=0.0.0.0"]