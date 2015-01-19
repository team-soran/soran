# soran

## installation

    $ pip install .

## run server

    $ cp exam.cfg.py.idst exam.cfg.py
    $ soran -c exam.cfg.py upgrade
    $ soran -c exam.cfg.py runserver

## db migration

    $ soran -c exam.cfg.py revision -m "your message"
