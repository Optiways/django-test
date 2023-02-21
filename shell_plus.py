MODULES = ["re", "json", "pprint"]

APPS_MODULES = [
    ("padam_django.apps.fleet.models", "Driver,Bus"),
    ("padam_django.apps.geography.models", "Place"),
    ("padam_django.apps.users.models", "User"),
]

IMPORTS = [f"import {module}" for module in MODULES]
FROM_IMPORTS = [f"from {module[0]} import {module[1]}" for module in APPS_MODULES]

NL = "\n"

c = get_config()  # noqa: F821 / pylint: disable=E0602

c.InteractiveShellApp.exec_lines = [
    *IMPORTS,
    *FROM_IMPORTS,
    "%load_ext autoreload",
    "%autoreload 2",
    "pretty = pprint.PrettyPrinter(indent=4).pprint",
]
c.InteractiveShell.colors = "Linux"
c.InteractiveShell.confirm_exit = False
c.TerminalInteractiveShell.autocall = 2
c.TerminalInteractiveShell.banner2 = (
    f"Welcome to shell+. If you want to change the config, "
    f"check shell_plus.py at the project root.{NL}"
    f"To pretty print your dict: 'pretty(my_dict)'{NL}"
    f"The following modules were loaded on startup:{NL}* "
    f"{f'{NL}* '.join(MODULES)}{NL}"
    f"* {','.join([m[1] for m in APPS_MODULES])}{NL}"
)
c.StoreMagics.autorestore = True
