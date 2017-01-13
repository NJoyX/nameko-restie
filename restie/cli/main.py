from __future__ import print_function

import argparse

from nameko.cli.main import setup_yaml_parser
from nameko.exceptions import CommandError, ConfigurationError

from . import commands


def setup_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    for command in commands.commands:
        command_parser = subparsers.add_parser(
            command.name, description=command.__doc__)
        command.init_parser(command_parser)
        command_parser.set_defaults(main=command.main)
    return parser


def main():
    parser = setup_parser()
    args = parser.parse_args()
    setup_yaml_parser()
    try:
        args.main(args)
    except (CommandError, ConfigurationError) as exc:
        print("Error: {}".format(exc))
