FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY cat-hub/ .

EXPOSE 5000

RUN apt-get update && apt-get install -y nodejs npm


RUN python setup.py

CMD ["python", "run.py"]