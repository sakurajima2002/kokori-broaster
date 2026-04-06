FROM node:20-slim AS node-build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npx tailwindcss -i ./static/src/input.css -o ./static/css/output.css

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=core.settings

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn  

COPY . .

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

COPY --from=node-build /app/static/css/output.css ./static/css/output.css

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
