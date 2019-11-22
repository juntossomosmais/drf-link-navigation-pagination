import django
from django.conf import settings


def pytest_assertrepr_compare(config, op, left, right):
    """
    More details at: https://stackoverflow.com/a/50625086/3899136
    """
    if op in ("==", "!="):
        return ["{0} {1} {2}".format(left, op, right)]


def pytest_configure():
    fake_app_location = "tests.support.fake_django_app"

    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
        SITE_ID=1,
        SECRET_KEY="not very secret in tests",
        USE_I18N=True,
        USE_L10N=True,
        USE_TZ=True,
        LANGUAGE_CODE="en-us",
        TIME_ZONE="UTC",
        STATIC_URL="/static/",
        ROOT_URLCONF=f"{fake_app_location}.urls",
        TEMPLATE_LOADERS=(
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ),
        MIDDLEWARE_CLASSES=(
            "django.middleware.common.CommonMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
        ),
        INSTALLED_APPS=(
            # Django admin
            "django.contrib.admin",
            # Django native apps
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.sites",
            "django.contrib.messages",
            "django.contrib.staticfiles",
            # DRF itself
            "rest_framework",
            # Our Application created only for testing purpose
            fake_app_location,
        ),
        PASSWORD_HASHERS=(
            "django.contrib.auth.hashers.SHA1PasswordHasher",
            "django.contrib.auth.hashers.PBKDF2PasswordHasher",
            "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
            "django.contrib.auth.hashers.BCryptPasswordHasher",
            "django.contrib.auth.hashers.MD5PasswordHasher",
            "django.contrib.auth.hashers.CryptPasswordHasher",
        ),
        REST_FRAMEWORK={
            "DEFAULT_PAGINATION_CLASS": "drf_link_navigation_pagination.LinkNavigationPagination",
            "PAGE_SIZE": 5,
        },
        ANONYMOUS_USER_ID=-1,
        AUTHENTICATION_BACKENDS=(
            "django.contrib.auth.backends.ModelBackend",
            "guardian.backends.ObjectPermissionBackend",
        ),
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [],
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.debug",
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ]
                },
            }
        ],
    )

    django.setup()
