FROM python:3.8

RUN pip install pipenv==2020.11.15

WORKDIR /app
ADD Pipfile Pipfile.lock ./

# The argument `pipenv_dev` controls whether or not to install development
# dependencies for the Django application. It should be left blank for
# production builds, and get set to '--dev' for non-production builds.
ARG pipenv_dev
RUN pipenv install --deploy --system $pipenv_dev

ENV DJANGO_ENVIRONMENT="production"
COPY . ./
EXPOSE 8000

WORKDIR /app/app_microservice
ENTRYPOINT ["gunicorn", "app_microservice.wsgi:application", \
    "--name=app-api", \
    "--bind=0.0.0.0:8000", \
    "--workers=4"]
