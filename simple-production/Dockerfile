FROM python:3.9

WORKDIR /app

COPY . /app

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install requests beautifulsoup4 python-dotenv

CMD ["python", "crows-pages.py"]


