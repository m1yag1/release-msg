# Release Reminder Message Creator

A very simple Flask application to be utlized by AWS Lambda to generate the reminder message for OpenStax releases.

## Development with Docker

### Install Docker and Docker Compose

Follow the instructions to install [Docker](https://docs.docker.com/install/).

Follow the instructions to install [Docker Compose](https://docs.docker.com/compose/install/).

### Run Docker Compose

    $ docker-compose up -d

## Deploying to AWS Lambda

> Note: You'll want to make sure you have your AWS credentials file at `~/.aws/credentials` filled out for deployment user `exercise-viewer`

The [Zappa](https://github.com/Miserlou/Zappa) project is used to package up the application and deploy it to AWS Lambda.

For deployment to AWS Lambda you'll want to run commands locally so the recommended method is to create a virtualenv and install the deploy requirements locally.

### Create a virtualenv

    $ python3 -m venv .venv

### Activate the virualenv

    $ source .venv/bin/activate

### Install the deploy requirements

    $ pip install -r requirements-deploy.txt

### Deploy the application

    $ zappa deploy dev
