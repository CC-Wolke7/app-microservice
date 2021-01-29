# App Microservice

## Development

### Docker

Development can be done in Docker without any external dependencies using [docker-compose](https://docs.docker.com/compose/reference/overview/).

For the first time running, you can bootstrap the local development environment with `bin/bootstrap.sh`.

After that, you can manage the environment with standard [docker-compose](https://docs.docker.com/compose/reference/overview/) commands. A few of the more common commands are listed below.

| Action                | Command                                                   |
| --------------------- | --------------------------------------------------------- |
| Bootstrap environment | `$ bin/bootstrap.sh`                                      |
| Start environment     | `$ docker-compose start`                                  |
| Stop environment      | `$ docker-compose stop`                                   |
| Attach to logs        | `$ docker-compose logs -f`                                |
| Python shell          | `$ docker-compose exec django ./manage.py shell`          |
| Apply DB Migrations   | `$ docker-compose exec django ./manage.py migrate`        |
| Make DB Migrations    | `$ docker-compose exec django ./manage.py makemigrations` |
| Destroy environment   | `$ docker-compose down -v`                                |

---

### Native

If you prefer not to develop with Docker, you can run the app natively on your system.

#### Dependencies:

- [Python 3.7+](https://www.python.org/)
- [Pipenv](https://pipenv.readthedocs.io/en/latest/)
- [MySQL](https://www.mysql.com/)

#### Steps:

- `$ brew install python pipenv`
- `$ brew install mysql` <sup>1</sup>
- `$ brew install mysql-connector-c` <sup>2</sup>
- `$ export PIPENV_VENV_IN_PROJECT=1`
- `$ pipenv sync --dev`
- `$ pipenv run app_microservice/manage.py runserver`

<sup>1</sup> _Make sure the MySQL service is running, and configure an appropriate database._

<sup>2</sup>_There is a bug with the MySQL python bindings on Mac OSX. See: [https://pypi.org/project/mysqlclient/](https://pypi.org/project/mysqlclient/)_

## Editor Setup

To install the pre-commit hooks that check and fix:

- trailing whitespaces
- file endings (forcing new lines)
- PE8 compliance
- style guide compliance

please run:

```shell
$ pipenv run pre-commit install
```

For VSCode, an appropriate `settings.json` is shipped as part of this repository.
