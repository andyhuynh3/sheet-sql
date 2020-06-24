from invoke import task


@task
def lint(c):
    c.run("pre-commit run --all-files")


@task
def build_dist(c):
    c.run("poetry build")


@task
def publish_dist(c):
    c.run("poetry publish")


@task
def test(c):
    c.run("pytest")
