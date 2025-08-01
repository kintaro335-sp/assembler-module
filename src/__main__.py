import os
from utils.arguments import get_arguments
from utils.files_utils import read_file
from interpreter.parser import parser
from environment import Machine
import time

machine = Machine()

instructions = []

def execute():
  global machine
  try:
    while(True):
      machine.execute_instructions()
      machine.next_tick()
      time.sleep(0.1)
  except KeyboardInterrupt:
    os._exit(0)

def declare():
  global instructions, machine
  machine = Machine(instructions)

def get_instructions(content: list[str]):
  global instructions
  for i in range(0, len(content)):
    result = parser.parse(content[i])
    if (result != None):
      instructions.append(result)

def main():
  args = get_arguments()
  file = args[0]
  content = read_file(file)
  get_instructions(content)
  declare()
  execute()

if __name__ == '__main__':
  main()