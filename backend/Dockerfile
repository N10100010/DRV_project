#FROM python:3.10-alpine
# not using alpine because of numpy
FROM python:3.10-slim

WORKDIR /usr/src/app

# camelot requirements
# Note that alpine has no apt-get:
# ref: https://github.com/gliderlabs/docker-alpine/blob/master/docs/usage.md#example
# ref: https://stackoverflow.com/a/45143116
RUN apt-get update && apt-get install -y \
    ghostscript \
    python3-tk

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-m", "flask", "--app", "app.app:app" , "--debug", "run"]

# Use `waitress` in prod: https://flask.palletsprojects.com/en/2.2.x/tutorial/deploy/#run-with-a-production-server
#CMD [ "waitress-serve", "--call", "app.app:app" ]