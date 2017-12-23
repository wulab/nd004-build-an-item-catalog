# Project: Build an Item Catalog

![screenshot](https://user-images.githubusercontent.com/592709/34283101-8016e5de-e6fc-11e7-9437-b03d67439d2f.png)

> An application that provides a list of items

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [Contribute](#contribute)
- [License](#license)

## Install

Docker Compose is required to run the script. Please refer to [Install Docker
Compose](https://docs.docker.com/compose/install/) if you don't have one on
your system.

Then, clone this repository:

    $ git clone https://github.com/wulab/nd004-build-an-item-catalog.git

## Usage

To run the app, issue the following command:

    $ cd nd004-build-an-item-catalog
    $ docker-compose up

The command will create an `app` service and start Flask built-in server on
port 8000. You will need to seed its SQLite database with initial data:

    $ docker-compose exec app flask initdb

Then, point your browser at http://localhost:8000/ to start using the app.

Press `Ctrl+C` to stop the service. If you want to clean up everything, use:

    $ docker-compose down --rmi local --volumes

## Contribute

PRs not accepted. However, you can fork this repository and modify it under
your account. To facilitate app development, there's a
`docker-compose.development.yml` file you that can use. It will mount your
`app/src` directory to the one in the container which you can edit.

    $ docker-compose -f docker-compose.yml -f docker-compose.development.yml up

## License

[MIT © Weera Wu.](LICENSE)
