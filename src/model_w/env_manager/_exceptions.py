try:
    from django.core.exceptions import ImproperlyConfigured
except ImportError:

    class ImproperlyConfigured(ValueError):  # type: ignore[no-redef]
        """
        Substitution for Django's ImproperlyConfigured error class
        """
