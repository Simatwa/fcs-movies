#!/usr/bin/python3
import os
import uvicorn
import click
from backend import app


@click.group()
def cli():
    """CLI for fcs-movies"""
    pass


@cli.command()
@click.argument(
    "port",
    required=False,
    type=click.INT,
    default=8000,
)
@click.option("--host", is_flag=True, help="Listen on all interfaces")
def runserver(port, host):
    uvicorn.run(app, host="0.0.0.0" if host else "127.0.0.1", port=port)


@cli.command()
def runtest():
    """Run unit-test using pytest"""
    os.system("pytest tests/test_*.py -xv")


if __name__ == "__main__":
    cli()
