from django.contrib.admin.apps import AdminConfig
from django.contrib.auth.apps import AuthConfig
from django.contrib.contenttypes.apps import ContentTypesConfig


class MongoAdminConfig(AdminConfig):
    """Use ObjectId primary keys for Django's admin models."""

    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"


class MongoAuthConfig(AuthConfig):
    """Use ObjectId primary keys for Django's authentication models."""

    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"


class MongoContentTypesConfig(ContentTypesConfig):
    """Use ObjectId primary keys for Django's content type models."""

    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
