# manage.py

import unittest

from flask import cli

from app import create_app


app = create_app()


@app.cli.command()
@cli.with_appcontext
def shell_plus():
    import os
    from IPython import embed

    embed(user_ns={"app": app, os: "os"})


if __name__ == "__main__":
    app.run(host="0.0.0.0")
