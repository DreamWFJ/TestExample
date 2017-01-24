from oslo_db.sqlalchemy import enginefacade


enginefacade.configure(
    sqlite_fk=True,
    max_retries=5,
    mysql_sql_mode='ANSI'
)


class SomeClass(object):
    pass

class MyContext(object):
    "User-defined context class."


def some_reader_api_function(context):
    with enginefacade.reader.using(context) as session:
        return session.query(SomeClass).all()


def some_writer_api_function(context, x, y):
    with enginefacade.writer.using(context) as session:
        session.add(SomeClass(x, y))


def run_some_database_calls():
    context = MyContext()

    results = some_reader_api_function(context)
    some_writer_api_function(context, 5, 10)



@enginefacade.transaction_context_provider
class MyContext1(object):
    "User-defined context class."

@enginefacade.reader
def some_reader_api_function1(context):
    return context.session.query(SomeClass).all()


@enginefacade.writer
def some_writer_api_function1(context, x, y):
    context.session.add(SomeClass(x, y))


def run_some_database_calls1():
    context = MyContext()

    results = some_reader_api_function1(context)
    some_writer_api_function1(context, 5, 10)


class DatabaseAccessLayer(object):

    @classmethod
    @enginefacade.reader
    def some_reader_api_function(cls, context):
        return context.session.query(SomeClass).all()

    @enginefacade.writer
    def some_writer_api_function(self, context, x, y):
        context.session.add(SomeClass(x, y))

# Base class for models usage
from oslo_db.sqlalchemy import models
class ProjectSomething(models.TimestampMixin,
                       models.ModelBase):
    id = models.Column(models.Integer, primary_key=True)
    pass


# DB API backend support
from oslo_config import cfg
from oslo_db import api as db_api

_BACKEND_MAPPING = {'sqlalchemy': 'project.db.sqlalchemy.api'}

IMPL = db_api.DBAPI.from_config(cfg.CONF, backend_mapping=_BACKEND_MAPPING)

def get_engine():
    return IMPL.get_engine()

def get_session():
    return IMPL.get_session()

# DB-API method
def do_something(somethind_id):
    return IMPL.do_something(somethind_id)
