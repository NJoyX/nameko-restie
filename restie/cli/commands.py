from nameko.cli.commands import Command, Run as NamekoRun


class Run(Command):
    """Run nameko services.  Given a python path to a module containing one or
        more nameko services, will host and run them. By default this will try to
        find classes that look like services (anything with nameko entrypoints),
        but a specific service can be specified via
        ``restiectl run module:ServiceClass``.
        """

    name = 'run'

    @staticmethod
    def init_parser(parser):
        parser = NamekoRun.init_parser(parser)
        parser.add_argument(
            '--listen',
            help='The address where the nameko web server should listen '
                 '(maybe ip:port format or file descriptor socket number (fileno)).'
        )
        return parser

    @staticmethod
    def main(args):
        from .run import main
        main(args)


commands = Command.__subclasses__()  # pylint: disable=E1101
