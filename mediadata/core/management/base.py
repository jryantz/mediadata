import argparse
import os
import sys
from argparse import ArgumentParser, HelpFormatter

import mediadata


class CommandError(Exception):
    """
    Exception class for a problem while executing a command.
    """

    def __init__(self, *args, returncode=1, **kwargs):
        self.returncode = returncode
        super().__init__(*args, **kwargs)


class BaseCommand:
    """
    The base class that is inherited by all command line commands.
    """

    help = ""

    def __init__(self, stdout=None, stderr=None):
        self.stdout = stdout or sys.stdout
        self.stderr = stderr or sys.stderr

    def get_version(self):
        """
        Return the mediadata version for all commands.
        """

        return mediadata.get_version()

    def create_parser(
        self, prog_name: str, subcommand: str, **kwargs
    ) -> ArgumentParser:
        """
        Create and return the parser for the command.
        """

        kwargs.setdefault("formatter_class", HelpFormatter)
        parser = ArgumentParser(
            prog="%s %s" % (os.path.basename(prog_name), subcommand),
            description=self.help or None,
            **kwargs,
        )
        parser.add_argument(
            "-V",
            "--version",
            action="version",
            version=self.get_version(),
            help="show application's version number and exit",
        )
        self.add_arguments(parser)
        return parser

    def add_arguments(self, parser):
        """
        Command arguments. Subclasses can implement this method.

        `parser.add_argument(...)` Parameters
        -------------------------------------

        `nargs`, Number of Arguments:

        - `3`: 3 values, can be any number you want
        - `?`: a single value, which can be optional
        - `*`: a flexible number of values, which will be gathered into a list
        - `+`: like *, but requiring at least one value
        - `argparse.REMAINDER`: all the values that are remaining in the command line
        """

        pass

    def print_help(self, prog_name, subcommand):
        """
        Print the help message for the command.
        """

        parser = self.create_parser(prog_name, subcommand)
        parser.print_help()

    def run(self, prog_name, argv):
        """
        Run the command.
        Print to stderr if an error occurs.
        """

        parser = self.create_parser(prog_name, argv[1])

        arguments = parser.parse_args(argv[2:])
        options = vars(arguments)
        args = options.pop("args", ())
        try:
            self.handle(*args, **options)
        except CommandError as e:
            if arguments.traceback:
                raise

            self.stderr.write("%s: %s" % (e.__class__.__name__, e))
            sys.exit(e.returncode)

    def handle(self, *args, **options):
        """
        Command logic. Subclasses must implement this method.
        """

        raise NotImplementedError(
            "subclasses of BaseCommand must provide a handle() method"
        )
