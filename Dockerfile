FROM python:3.10.9

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_ENV=production

WORKDIR /app/frontend/build

RUN npm install -g serve

EXPOSE 80

CMD ["python", "../app.py"]   
