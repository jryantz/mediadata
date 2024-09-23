"""
Application management module
"""

import os
import pkgutil
import sys
from argparse import ArgumentParser
from difflib import get_close_matches
from importlib import import_module

import mediadata
from mediadata.core.management.base import (
    BaseCommand,
    CommandError,
)


def find_commands(management_dir: str) -> list[str]:
    """
    Traverses the management commands directory and loads
    available commands
    """

    command_dir = os.path.join(management_dir, "commands")
    return [
        name
        for _, name, is_pkg in pkgutil.iter_modules([command_dir])
        if not is_pkg and not name.startswith("_")
    ]


def load_command_class(name):
    """
    Loads a command class and returns it
    """

    module = import_module(f"mediadata.core.management.commands.{name}")
    return module.Command()


def get_commands() -> list[str]:
    """
    Returns a list of available commands
    """

    return list(find_commands(__path__[0]))


class ManagementUtility:
    """
    Primary utility to control the execution flow of the application.
    """

    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        if self.prog_name == "__main__.py":
            self.prog_name = "python -m mediadata"

    def help(self, commands_only=False) -> str:
        """
        Return the application's main help text.
        """

        if commands_only:
            usage = sorted(get_commands())
        else:
            usage = [
                f"usage: {self.prog_name} <subcommand>",
                "",
                f"Type '{self.prog_name} help <subcommand>' for help with a specific subcommand.",
                "",
                "subcommands:",
            ]
            for command in get_commands():
                usage.append(command)

        return "\n".join(usage)

    def fetch_command(self, subcommand: str):
        """
        Try to fetch the subcommand. If there is no match, print a list of similar commands.
        """

        commands = get_commands()

        if subcommand in commands:
            app_name = "mediadata.core"
        else:
            possible_matches = get_close_matches(subcommand, commands)
            sys.stderr.write(f"Unknown command: {subcommand}")
            if possible_matches:
                sys.stderr.write(f". Did you mean {possible_matches[0]}?")
            sys.stderr.write(f"\nType '{self.prog_name} help' for usage.\n")
            sys.exit(1)

        if isinstance(app_name, BaseCommand):
            command = app_name
        else:
            command = load_command_class(subcommand)
        return command

    def execute(self):
        """
        Discover the executed command, create a parser, and run the command.
        """

        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = "help"

        parser = ArgumentParser(
            prog=self.prog_name,
            usage="%(prog)s subcommand [options] [args]",
            add_help=False,
            allow_abbrev=False,
        )
        try:
            _, args = parser.parse_known_args(self.argv[2:])
        except CommandError:
            pass

        if subcommand == "help":
            if "--commands" in args:
                sys.stdout.write(self.help(commands_only=True) + "\n")
            elif not args:
                sys.stdout.write(self.help() + "\n")
            else:
                self.fetch_command(args[0]).print_help(self.prog_name, args[0])
        elif subcommand == "version":
            sys.stdout.write(mediadata.get_version() + "\n")
        else:
            self.fetch_command(subcommand).run(self.prog_name, self.argv)


def execute(argv=None):
    """
    Start the application from the command line.
    """

    utility = ManagementUtility(argv)
    utility.execute()
