FROM python:3.10-slim
# not using alpine because of numpy

# Ref: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

WORKDIR /usr/src/app

# camelot requirements
RUN apt-get update && apt-get install -y \
    ghostscript \
    python3-tk

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Note that interface "0.0.0.0" has to be used
CMD [ "python", "-m", "flask", "--app", "app.app:app" , "--debug", "run", "--host", "0.0.0.0"]

# Use e.g. `waitress` in prod: https://flask.palletsprojects.com/en/2.2.x/tutorial/deploy/#run-with-a-production-server
#CMD [ "waitress-serve", "--call", "app.app:app" ]