# Server For Our Booking Platform

## <ins>Table Of Content</ins>
- Project Purpose
- Setup Instructions

## <ins>Project Purpose</ins>
This is the backend of our booking platform, which helps you book trips for your group.

## <ins>Setup Instructions</ins>

### Prerequisites
- Python 3.11
- Docker
- Git

### Installation Locally
1. First, the app need to downloaded locally to a specified directory.

```bash
git clone 
cd /your/path/to/booking-platform
```

2. The docker-compose.yml file need to be set up in the correct directory: touch /you/path/to/booking-platform/docker-compose.yml And the below content need to be added there and be check from a yaml checker for its correctness: nano /your/path/to/booking-platform/docker-compose.yml

```bash
touch /your/path/to/booking-platform/docker-compose.yml
nano /your/path/to/booking-platform/docker-compose.yml
```

```bash
services:
  backend:
    build: 
      context: ./booking-platform-service
      dockerfile: Dockerfile.server
    ports:
      - "8000:8000"
    environment:
      - FLASK_APP=app.py
    depends_on:
      - db
    networks:
      - my-network
  
  db:
    image: postgres:latest
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASS}
      POSTGRES_DB: ${DB_NAME}
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data
    networks:
      - my-network

networks:
  my-network:

volumes:
  db_data:
```

3. The Dockerfile needs to be also created:

```bash
touch /your/path/to/booking-platform/booking-platform-server/Dockerfile.server
nano /your/path/to/booking-platform/booking-platform-server/Dockerfile.server
```

```bash
FROM python:3.11-alpine

# Update the package list and install libpq-dev and gcc
RUN apk update && \
    apk add --no-cache \
        libpq \
        gcc \
        musl-dev \
        postgresql-dev

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
```

4. Start the docker and your maschine from the user interface and then start the application using the terminal.

```bash 
cd /your/path/to/booking-platform
sudo docker compose build --no-cache && sudo docker compose up --build -d
```