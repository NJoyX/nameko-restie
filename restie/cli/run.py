from __future__ import print_function

import eventlet

eventlet.monkey_patch()  # noqa (code before rest of imports)

import logging
import logging.config
import sys

import yaml
from nameko.constants import AMQP_URI_CONFIG_KEY, WEB_SERVER_CONFIG_KEY
from nameko.cli.run import import_service, run

logger = logging.getLogger(__name__)


def main(args):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

    if args.config:
        with open(args.config) as fle:
            config = yaml.load(fle)
    else:
        config = {
            AMQP_URI_CONFIG_KEY: args.broker
        }

    if args.listen:
        config[WEB_SERVER_CONFIG_KEY] = args.listen

    if "LOGGING" in config:
        logging.config.dictConfig(config['LOGGING'])
    else:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    services = []
    for path in args.services:
        services.extend(
            import_service(path)
        )

    run(services, config, backdoor_port=args.backdoor_port)
