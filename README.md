# Server For Our Booking Platform

## Table Of Content
- Project Purpose
- Setup Instructions

## <ins>Project Purpose</ins>
This is the backend of our booking platform, which helps you book trips for your group.

## Setup Instructions

### Prerequisites
- Python 3.11
- Docker
- Git

### Installation Locally
1. First Clone the workspace repo
```bash 
git clone https://github.com/Hackathon-VGI/workspace.git
cd /your/path/to/workspace
```


2. Now the app need to be downloaded locally inside the workspace directory.

```bash
git clone https://github.com/Hackathon-VGI/booking-platform-server.git
cd /your/path/to/workspace/booking-platform-server
```

3. Start the docker and your machine from the user interface and then start the application using the terminal.

```bash 
cd /your/path/to/workspace
sudo docker compose build --no-cache && sudo docker compose up --build -d
```