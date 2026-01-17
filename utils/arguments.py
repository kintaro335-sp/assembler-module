import sys


def get_arguments() -> list:
  arguments = sys.argv
  arguments.pop(0)
  return arguments
