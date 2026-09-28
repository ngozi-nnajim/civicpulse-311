"""Smoke tests: prove the package is installed and importable."""

from importlib.metadata import version  # reads the package version recorded when it was installed

import civicpulse  # if the folder layout or packaging is broken, this line, and the test, fail


def test_package_has_docstring() -> None:
    """The package explains what it is."""
    assert civicpulse.__doc__  # an empty or missing docstring is "falsy", so this would fail


def test_installed_version_is_set() -> None:
    """pip knows the package's version.

    (it comes from pyproject.toml, the single source of truth)."""
    assert version("civicpulse")  # raises an error if the package isn't installed at all
