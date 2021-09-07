"""
NOTE:
    the below code is to be maintained Python 2.x-compatible
    as the whole Cookiecutter Django project initialization
    can potentially be run in Python 2.x environment
    (at least so we presume in `pre_gen_project.py`).

TODO: ? restrict Cookiecutter Django project initialization to Python 3.x environments only
"""
from __future__ import print_function

import os
import random
import shutil
import string

try:
    # Inspired by
    # https://github.com/django/django/blob/master/django/utils/crypto.py
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "


def generate_random_string(
    length, using_digits=False, using_ascii_letters=False, using_punctuation=False
):
    """
    Example:
        opting out for 50 symbol-long, [a-z][A-Z][0-9] string
        would yield log_2((26+26+50)^50) ~= 334 bit strength.
    """
    if not using_sysrandom:
        return None

    symbols = []
    if using_digits:
        symbols += string.digits
    if using_ascii_letters:
        symbols += string.ascii_letters
    if using_punctuation:
        all_punctuation = set(string.punctuation)
        # These symbols can cause issues in environment variables
        unsuitable = {"'", '"', "\\", "$"}
        suitable = all_punctuation.difference(unsuitable)
        symbols += "".join(suitable)
    return "".join([random.choice(symbols) for _ in range(length)])


def set_flag(file_path, flag, formatted=None, value=None, *args, **kwargs):
    if not value:
        random_string = generate_random_string(*args, **kwargs)
        if formatted is not None:
            random_string = formatted.format(random_string)
        value = random_string

    with open(file_path, "r+") as f:
        file_contents = f.read().replace(flag, value)
        f.seek(0)
        f.write(file_contents)
        f.truncate()

    return value


def set_django_secret_key(file_path):
    return set_flag(
        file_path,
        "!!!SET DJANGO_SECRET_KEY!!!",
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )


def set_django_admin_url(file_path):
    return set_flag(
        file_path,
        "!!!SET DJANGO_ADMIN_URL!!!",
        formatted="{}/",
        length=32,
        using_digits=True,
        using_ascii_letters=True,
    )


def set_postgres_user(file_path):
    value = generate_random_string(length=32, using_ascii_letters=True)
    return set_flag(file_path, "!!!SET POSTGRES_USER!!!", value=value)


def set_postgres_password(file_path):
    value = generate_random_string(length=32, using_ascii_letters=True)
    return set_flag(
        file_path,
        "!!!SET POSTGRES_PASSWORD!!!",
        value=value,
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )


def set_celery_flower_user(file_path):
    value = generate_random_string(length=32, using_ascii_letters=True)
    return set_flag(
        file_path, "!!!SET CELERY_FLOWER_USER!!!", value=value
    )


def set_celery_flower_password(file_path):
    value = generate_random_string(length=32, using_ascii_letters=True)
    return set_flag(
        file_path,
        "!!!SET CELERY_FLOWER_PASSWORD!!!",
        value=value,
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )



def main():
    local_django_envs_path = os.path.join(".envs", ".local", ".django")
    production_django_envs_path = os.path.join(".envs", ".production", ".django")
    local_postgres_envs_path = os.path.join(".envs", ".local", ".postgres")
    production_postgres_envs_path = os.path.join(".envs", ".production", ".postgres")

    set_django_secret_key(production_django_envs_path)
    set_django_admin_url(production_django_envs_path)

    set_postgres_user(local_postgres_envs_path)
    set_postgres_password(local_postgres_envs_path)
    set_postgres_user(production_postgres_envs_path)
    set_postgres_password(production_postgres_envs_path)

    set_celery_flower_user(local_django_envs_path)
    set_celery_flower_password(local_django_envs_path)
    set_celery_flower_user(production_django_envs_path)
    set_celery_flower_password(production_django_envs_path)

    set_django_secret_key(os.path.join("config", "settings", "local.py"))
    set_django_secret_key(os.path.join("config", "settings", "test.py"))

    if "{{ cookiecutter.ci_tool }}".lower() != "travis":
        os.remove(".travis.yml")

    if "{{ cookiecutter.ci_tool }}".lower() != "gitlab":
        os.remove(".gitlab-ci.yml")

    if "{{ cookiecutter.ci_tool }}".lower() != "github":
        shutil.rmtree(".github")

    print(SUCCESS + "Project initialized, keep up the good work!" + TERMINATOR)


if __name__ == "__main__":
    main()
