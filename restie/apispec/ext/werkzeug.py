import re

from apispec import Path, utils
from six.moves import urllib

# from flask-restplus
RE_URL = re.compile(r'<(?:[^:<>]+:)?([^<>]+)>')


def werkzeugpath2swagger(path):
    """Convert a Werkzeug URL rule to an OpenAPI-compliant path.

    :param str path: Werkzeug path template.
    """
    return RE_URL.sub(r'{\1}', path)


def path_from_view(spec, view, rule, **kwargs):
    """Path helper that allows passing a Werkzeug view function."""
    path = werkzeugpath2swagger(rule.rule)
    path = urllib.parse.urljoin('/', path.lstrip('/'))
    operations = utils.load_operations_from_docstring(view.__doc__)
    path = Path(path=path, operations=operations)
    return path


def setup(spec):
    """Setup for the plugin."""
    spec.register_path_helper(path_from_view)
