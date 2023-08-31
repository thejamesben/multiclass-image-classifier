FROM python:3.10.9

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs

WORKDIR /app/frontend/build

RUN npm install -g serve

WORKDIR /app

EXPOSE 80

CMD ["python", "app.py"]








