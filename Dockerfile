FROM python:3.7

# Disable .pyc file to avoid python version conflict and reduce image size
ENV PYTHONDONTWRITEBYTECODE 1
# Disable buffer to have an immediate output and easier debugging
ENV PYTHONUNBUFFERED 1
ENV WORKDIR=/app/
ENV ENVIRONMENT=dev
ENV PORT=8000

COPY /requirements /requirements/

# Install pipenv and compilation dependencies
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements/dev.txt

# Install dependencies to dev
RUN apt-get update && apt-get install -y vim zsh
RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true

# Define work directory
WORKDIR $WORKDIR
COPY . $WORKDIR

EXPOSE $PORT

CMD python manage.py runserver_plus 0.0.0.0:$PORT
