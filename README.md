# Project: Build an Item Catalog

![screenshot](https://user-images.githubusercontent.com/592709/33794751-95015aa8-dd04-11e7-94bf-7ebdc217c670.png)

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

    $ git clone https://github.com/wulab/nd004-logs-analysis.git

## Usage

To run the reporting tool, issue the following command:

    $ cd nd004-movie-trailer-website
    $ docker-compose run --rm app

The command will create a `db` service and seed it with initial data. Then, an
`app` service that hosts the script to generate reports from that data will be
created. Finally, you'll see 3 reports printed out on your console.

If you want to clean up after running the reporting tool, use:

    $ docker-compose down --rmi local --volumes

## Contribute

PRs not accepted. However, you can fork this repository and modify it under
your account. To facilitate script development, there's a
`docker-compose.development.yml` file you that can use. It will let you edit
the `logs_analysis.py` file inside the container.

    $ docker-compose -f docker-compose.yml -f docker-compose.development.yml run --rm app /bin/sh
    /usr/src/app # python logs_analysis.py

## License

[MIT © Weera Wu.](LICENSE)
