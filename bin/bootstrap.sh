#!/bin/bash
set -ueo pipefail

PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." > /dev/null && pwd )"

promptyn () {
    while true; do
        read -rp "$1 " yn
        case $yn in
            [Yy]* ) return 0;;
            [Nn]* ) return 1;;
            * ) echo "Please answer yes or no.";;
        esac
    done
}

abort() {
    tput setaf 1
    echo "$1"
    tput sgr0
    exit 1
}

header() {
    echo
    tput setaf 5
    echo "$1"
    tput sgr0
}

cd "$PROJECT_ROOT"

# Test that user has the docker tools installed.
pgrep -f docker > /dev/null \
    || abort "The docker daemon is not running. Please start it and try again."
command -v docker-compose > /dev/null \
    || abort "Could not find 'docker-compose'. Please install docker and try again."

header "[ Building Containers ]"
docker-compose build

header "[ Starting Services ]"
docker-compose up -d

echo "Pausing 15 seconds for MySQL to initialize the database..."
sleep 15s

echo "Restarting django container"
docker-compose restart django

header "[ Running Database Migrations ]"
docker-compose exec django ./manage.py migrate

header "[ Creating Superuser ]"
if promptyn "Create a superuser (recommended)? [y/n] >"; then
    docker-compose exec django ./manage.py createsuperuser
fi

header "[ Status ]"
echo "The following containers are now running:"
echo
docker-compose ps

echo
header "Setup complete!"
echo
echo "Access the app-api with a web browser:"
echo "  $ open http://localhost:8100/"
echo
echo "Perform future management tasks with docker-compose:"
echo "  $ docker-compose help"
echo
echo "Run Django management commands with the following:"
echo "  $ docker-compose exec django ./manage.py <command>"
echo
echo "View logs with docker-compose logs:"
echo "  $ docker-compose logs -f"
echo
if promptyn "Attach to logs now? [y/n] >"; then
    docker-compose logs -f
fi
