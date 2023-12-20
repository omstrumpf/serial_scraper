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
RUN apk add --no-cache --virtual .build-deps gcc libc-dev libxslt-dev
RUN apk add --no-cache bash python3 py3-pip py3-lxml libxslt

# Set up python venv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir pipenv lxml
RUN set -ex && pipenv install --deploy --system

# Remove build dependencies
RUN apk del .build-deps

# Enable crontab
RUN /usr/bin/crontab /app/crontab

# Entry
CMD ["/bin/bash", "entry.sh"]
