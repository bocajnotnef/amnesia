#!/usr/bin/env python3
# other note taking / journal utils don't do what I want
# so we're gonna hack together our own

import argparse
import datetime
import json
import logging
import os
import pickle
import pypandoc
import subprocess
import sys

from pathlib import Path
from typing import Optional, List

# cross platform (probably)
# thanks to https://stackoverflow.com/questions/4028904/how-to-get-the-home-directory-in-python
HOMEDIR = str(Path.home())
SUBDIRECTORY = "amnesia-testing"
__version__ = "v.nope" # TODO: verioneer

class State:
    "hold all the program state, to make it easier to save/load"

    def __init__(self):
        self.notebooks = {}


class DefaultProgramForOS:
    "to open a thing in system default editor"
    # adapted from https://stackoverflow.com/questions/434597/open-document-with-default-application-in-python

    @staticmethod
    def open(filepath) -> None:
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', filepath))
        elif os.name == 'nt': # For Windows
            # ignore the problem on this line because the method doesn't exist on Darwin/Posix
            os.startfile(filepath) # pylint: disable=E1101
        elif os.name == 'posix': # For Linux, Mac, etc.
            subprocess.call(('xdg-open', filepath))


class Notebook:
    "A collection of notes"
    def __init__(self, name, path=None):
        self.name = name
        self.path = path
        pass

    @staticmethod
    def create_notebook(args, state: State):

        logging.info("creating notebook")

        path = None
        if args.path is not None:
            path = args.path
        else:
            path = args.name

        if not os.path.exists(path):
            logging.info(f"created directory {path}")
            os.makedirs(path)

        state.notebooks[args.name] = (Notebook(args.name, path))

        return state.notebooks[args.name]

    @staticmethod
    def add_args_to_subparsers(subparsers):

        notebook_parser: argparse.ArgumentParser = subparsers.add_parser('notebook')

        notebook_subparsers = notebook_parser.add_subparsers()

        create_parser: argparse.ArgumentParser = notebook_subparsers.add_parser('create')
        create_parser.add_argument('name', help="the name for the notebook to create")
        create_parser.add_argument('--path', help="optional path to store the notebook in")
        create_parser.set_defaults(func=Notebook.create_notebook)


class WeeklyNotes:

    subdir = "weekly_notes"

    @staticmethod
    def makeWeeklyNote(forNotebook):
        logging.info(f"so you called makeWeeklyNote {forNotebook}")

    @staticmethod
    def addArgsToParser(parser: argparse.ArgumentParser):
        parser.add_argument('notebook_name', help="the notebook to put the note into")

    @staticmethod
    def determineMostRecentMonday(curr_date) -> str:
        mostRecentMonday = curr_date - datetime.timedelta(days=-curr_date.weekday(), weeks=1)

        curr_datestring = datetime.date.strftime(curr_date, r"%Y-%m-%d")
        mondatestring = datetime.date.strftime(mostRecentMonday, r"%Y-%m-%d")

        logging.info(f"today is {curr_datestring}, so most recent monday is {mondatestring}")

        return mondatestring

    @staticmethod
    def openWeeklyNoteFile(curr_date, os_source, default_source) -> None:
        mondate = WeeklyNotes.determineMostRecentMonday(curr_date)

        filepath = f"{HOMEDIR}/{SUBDIRECTORY}/{mondate}.md"
        noteDir = os_source.path.dirname(filepath)

        if not os_source.path.exists(noteDir):
            logging.info(f"created directory {noteDir}")
            os_source.makedirs(noteDir)

        if not Path(filepath).exists():
            with open(filepath, 'w') as _:
                pass # just need to make it exist

        logging.info("opening file with system default editor")
        default_source.open(filepath)

    @staticmethod
    def run(args: argparse.Namespace, state: State, curr_date=datetime.datetime.now(), os_source=os, default_source=DefaultProgramForOS):
        WeeklyNotes.openWeeklyNoteFile(curr_date, os_source, default_source)


def getArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('--debug', help="enable debugging mode", action="store_true")
    parser.add_argument('--version', action='version', help="output the version and exit immediately", version=__version__)

    subparsers = parser.add_subparsers()

    weekly_notes_parser = subparsers.add_parser('weekly_notes')
    WeeklyNotes.addArgsToParser(weekly_notes_parser)
    weekly_notes_parser.set_defaults(func=WeeklyNotes.run)

    Notebook.add_args_to_subparsers(subparsers)

    return parser.parse_args()


def main(args, notebooks=None):
    logging.basicConfig(format=r"%(asctime)s %(module)s::%(funcName)s: %(message)s", datefmt=r"%Y-%m-%d %H:%M:%S")

    state = State()

    if args.debug:
        logging.getLogger().setLevel(logging.INFO)

    args.func(args, state)

if __name__ == "__main__":
    args = getArgs()
    main(args)
