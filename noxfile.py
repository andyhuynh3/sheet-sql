import os
import tempfile
from typing import Any

import nox
from nox.sessions import Session

PYTHON = ["3.7", "3.8"]
locations = "src", "tests", "noxfile.py"
nox.options.sessions = "lint", "tests"


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """
    Install packages constrained by Poetry's lock file.

    This function is a wrapper for nox.sessions.Session.install. It
    invokes pip to install packages inside of the session's virtualenv.
    Additionally, pip is passed a constraints file generated from
    Poetry's lock file, to ensure that the packages are pinned to the
    versions specified in poetry.lock. This allows you to manage the
    packages as Poetry development dependencies.

    Arguments:
        session: The Session object.
        args: Command-line arguments for pip.
        kwargs: Additional keyword arguments for Session.install.
    """
    req_path = os.path.join(tempfile.gettempdir(), os.urandom(24).hex())
    session.run(
        "poetry",
        "export",
        "--dev",
        "--format=requirements.txt",
        f"--output={req_path}",
        external=True,
    )
    session.install(f"--constraint={req_path}", *args, **kwargs)
    os.unlink(req_path)


@nox.session(python=PYTHON)
def tests(session):
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


@nox.session(python=PYTHON)
def lint(session):
    args = session.posargs or locations
    session.install("flake8", "flake8-black")
    session.run("flake8", *args)


@nox.session(python=PYTHON)
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)
