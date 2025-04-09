FROM python:3.11-slim

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "bot"]
