""":mod:`soran.datetime` --- datetime
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use this module instead :mod:`datetime` to confirm all time related values are
in UTC timezone. because :mod:`datetime` return a naive datetime which
dosen't contain a timezone by default.

.. sourcecode:: python

   >>> from soran.datetime import datetime, now
   >>> datetime(2015, 1, 1, 1)
   datetime.datetime(2015, 1, 1, 1, 0,
                     tzinfo=<iso8601.iso8601.Utc object at 0x10d44eef0>)
   >>> now()
   datetime.datetime(2015, 5, 31, 11, 54, 44, 930324,
                     tzinfo=<iso8601.iso8601.Utc object at 0x10d44eef0>)

"""
from datetime import date, datetime as py_datetime
from functools import singledispatch, partial

from annotation.typed import typechecked
from iso8601 import parse_date
from iso8601.iso8601 import UTC


#: Replacement of :class:`~datetime.datetime` with UTC timezone.
datetime = partial(py_datetime, tzinfo=UTC)


@typechecked
def now() -> py_datetime:
    """Return now as a :class:`~datetime.datetime` with UTC timezone.

    :return:
    """
    return py_datetime.now(tz=UTC)


@singledispatch
def parse(t):
    """Parse datetime to string, string to datetime.

    :param t:
    :return:
    """
    return t


@parse.register(date)
@parse.register(py_datetime)
def _(t):
    if t.tzinfo is None:
        raise ValueError("Can't parse naive datetime.")
    return t.astimezone(tz=UTC).isoformat()


@parse.register(str)
def _(t):
    return parse_date(t, datetime=UTC)
