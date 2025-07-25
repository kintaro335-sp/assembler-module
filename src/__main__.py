import os
from utils.arguments import get_arguments
from utils.files_utils import read_file
from interpreter.parser import parser
from environment import Machine

machine = Machine()

instructions = []

# class MODULE_EXEC:
#   def __init__(self, instructions = []) -> None:
#     self.module = MODULE()
#     self.step = 0
#     self.instructions = instructions
    
#   def execute_instruction(self):
#     pass

# def set_decalration(inst):
#   global aux_instructions
#   print(inst)
#   match inst[0]:
#     case 'STRING':
#       strings[inst[1]] = inst[2]
#       types[inst[1]] = 'STRING'
#     case 'MODULE':
#       types[inst[1]] = 'MODULE'

#     case 'MOV':
#       aux_instructions.append(inst)
#     case 'SUB':
#       aux_instructions.append(inst)
#     case 'ADD':
#       aux_instructions.append(inst)
#     case 'JEZ':
#       aux_instructions.append(inst)
#     case 'JNZ':
#       aux_instructions.append(inst)
#     case 'JGZ':
#       aux_instructions.append(inst)
#     case 'JLZ':
#       aux_instructions.append(inst)
#     case 'JMP':
#       aux_instructions.append(inst)
#     case 'LABEL':
#       aux_instructions.append(inst)
      
#   pass

def execute():
  global machine
  try:
    while(True):
      machine.execute_instructions()
      machine.next_tick()
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