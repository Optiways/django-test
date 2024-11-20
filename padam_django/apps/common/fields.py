from django.db import models


class TsCreateField(models.DateTimeField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("auto_now_add", True)
        kwargs.setdefault("auto_now", False)
        kwargs.setdefault("verbose_name", "Creation date")
        kwargs.setdefault("help_text", "Date at which the object was created.")
        super().__init__(*args, **kwargs)


class TsUpdateField(models.DateTimeField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("auto_now", True)
        kwargs.setdefault("verbose_name", "Last update date")
        kwargs.setdefault("help_text", "Date at which the object was updated.")
        super().__init__(*args, **kwargs)
