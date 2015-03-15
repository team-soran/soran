# soran

## table of contents

 - [installation](#installation)
   - [Prerequisites](#prerequisites)
   - [dependencies](#dependencies)

## installation

### Prerequisites

    $ npm install -g grunt-cli
    $ npm install
    $ grunt selenium:download

### dependencies

    $ pip install .

## run server

    $ cp exam.cfg.py.dist exam.cfg.py
    $ soran -c exam.cfg.py upgrade
    $ soran -c exam.cfg.py runserver

## db migration

    $ soran -c exam.cfg.py revision -m "your message"
