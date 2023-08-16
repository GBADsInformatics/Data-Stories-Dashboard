# Base image - tried a few others, this one was the easiest and most resilient
FROM python:3.10.0-slim-buster

# Specify root directory in image
WORKDIR /app/dash

# Install needed packages
RUN apt update && \
 apt install -y gcc musl-dev postgresql python-psycopg2 libpq-dev && \
 rm -rf /var/lib/apt/lists/*

# Installing python requirements
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt --no-cache-dir

# Copy dash files to image
COPY . /app/dash

# Specifying the dashboard command
CMD ["waitress-serve","--host=0.0.0.0","--port=80","--call","index:returnApp"]


