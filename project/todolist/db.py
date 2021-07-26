import psycopg2
import datetime

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect('dbname=todo')
    return g.db

def close_db(e=None):
    db=g.pop('db',None)
    if db is not None:
        db.close()
        
def commit_db(string,lst):
    db=get_db()
    cursor=db.cursor()
    cursor.execute(string,lst)
    db.commit()
    return db

def init_db():
    db=get_db()
    f=current_app.open_resource("todo.sql")
    sql_code=f.read().decode("ascii")
    cur=db.cursor()
    cur.execute(sql_code)
    cur.close()
    db.commit()

@click.command('initdb',help='initialise the database')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('DB initialised')
    
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)       