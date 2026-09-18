"""
Flask CLI Command Extensions
"""
import click
from service.models import db


@click.command("db-create")
def db_create():
    """Recreates a local development database"""
    db.drop_all()
    db.create_all()
    db.session.commit()
