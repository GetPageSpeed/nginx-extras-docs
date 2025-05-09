"""hooks for MkDocs to auto-update the copyright year."""

from datetime import datetime


def on_config(config, **kwargs):
    """
    MkDocs event hook: runs immediately after loading mkdocs.yml.
    Replace the `{year}` placeholder in config.copyright with the current year.
    """
    config.copyright = config.copyright.format(year=datetime.now().year)
    return config
