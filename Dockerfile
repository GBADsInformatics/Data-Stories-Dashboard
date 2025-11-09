# Base image - tried a few others, this one was the easiest and most resilient
FROM python:3.10-slim-bookworm

# Specify root directory in image
WORKDIR /app/dash

# Install needed packages (Debian names)
# - musl-dev is an Alpine package; use build-essential on Debian
# - python-psycopg2 is not a Debian package name; use libpq-dev + python3-dev
RUN apt-get update && \
	apt-get install -y --no-install-recommends \
		gcc build-essential libpq-dev python3-dev postgresql-client && \
	rm -rf /var/lib/apt/lists/*

# Installing python requirements
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt --no-cache-dir

# Copy dash files to image
COPY . /app/dash

# Specifying the dashboard command
CMD ["waitress-serve","--host=0.0.0.0","--port=80","--call","index:returnApp"]


