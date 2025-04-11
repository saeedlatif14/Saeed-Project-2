# FROM ubuntu:20.04
# RUN apt-get update -y
# COPY . /app
# WORKDIR /app
# RUN set -xe \
#     && apt-get update -y \
#     && apt-get install -y python3-pip \
#     && apt-get install -y mysql-client 
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
# EXPOSE 8080
# ENTRYPOINT [ "python3" ]
# CMD [ "app.py" ]


FROM ubuntu:20.04

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev curl mysql-client && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy app code
COPY . /app

# Upgrade pip and install Python packages
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Flask environment
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# Expose the Flask app port
EXPOSE 8080

# Entry point to run the app via Flask CLI
CMD ["flask", "run"]
