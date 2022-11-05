FROM alpine:latest

# Set up workdir
WORKDIR /app
ADD scraper /app/scraper/
ADD Pipfile Pipfile
ADD Pipfile.lock Pipfile.lock
ADD entry.sh entry.sh
ADD crontab crontab
ADD token.pickle token.pickle

# Install Dependencies
RUN apk --no-cache add bash python3 py3-pip py3-lxml
RUN pip3 install --upgrade pip
RUN pip3 install pipenv
RUN set -ex && pipenv install --deploy --system

# Enable crontab
RUN /usr/bin/crontab /app/crontab

# Entry
CMD ["/bin/bash", "entry.sh"]
