# soran

## table of contents

 - [Installation](#installation)
   - [Prerequisites](#prerequisites)
   - [Dependencies](#dependencies)
 - [Run server](#run-server)
 - [DB migration](#db-migration)
 - [Documentation](#documentation)

## Installation

### Prerequisites

- [flake8](https://flake8.readthedocs.org/en/2.3.0/)
- [import-order](https://github.com/spoqa/import-order)
- [python3.4](https://docs.python.org/3/)
- [bower](http://bower.io/)

### Dependencies

 - Install lint
 
   ```
   $ pip install flake8 && pip install import-order
   $ ln -s $(pwd)/hooks/pre-commit .git/hooks/pre-commit
   ```
 - Install bower depedencies

   ```
   $ bower install
   ```
 - Install python libraries
 
   ```
   $ pip install . && pip install -e .[tests]
   ```
## Run server

To configure your settings, copy `exam.cfg.py.dist` to `exam.cfg.py`. 

    $ cp exam.cfg.py.dist exam.cfg.py

And you can easily pass your configuration through `-c` option.

    $ soran -c exam.cfg.py runserver

## DB migration

To migrate your DB changes, create revision by `revision` command.

    $ soran -c exam.cfg.py revision -m "your message"

Or you can upgrade/downgrae your revision.

    $ soran -c exam.cfg.py upgrade
    $ soran -c exam.cfg.py downgrade -1

## Documentation

Use [Sphinx](http://sphinx-doc.org/) to create document for sourcodes,
database models, API, and etc.

