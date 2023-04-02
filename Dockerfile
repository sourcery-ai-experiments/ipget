FROM python:3.11-alpine as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base as python-deps

# Install dependencies into .venv
RUN pip3 install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base as runtime

# Fix logging output
ENV PYTHONUNBUFFERED=1

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# THIS BREAKS LOGGING with permissions errors writing the log file
# Create and switch to a new user
# RUN adduser -D -u 5000 appuser # alpine
# WORKDIR /home/appuser
# USER appuser

# Install application into container
COPY ./src /home/appuser/app

# Run the application
ENTRYPOINT ["python", "/home/appuser/app/app.py"]
