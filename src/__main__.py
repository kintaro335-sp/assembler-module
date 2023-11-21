from utils.arguments import get_arguments
from utils.files_utils import read_file
from interpreter.parser import parser
from environment.module import MODULE
from threading import Thread

types = {}

modules = {}

strings = {}

instructions = []

aux_instructions = []

class MODULE_EXEC:
  def __init__(self, instructions = []) -> None:
    self.module = MODULE(instructions)
    self.step = 0
    self.instructions = instructions
    
  def execute_instruction(self):
    pass


def module_declaration():
  pass

def set_decalration(inst):
  global aux_instructions
  print(inst)
  match inst[0]:
    case 'STRING':
      strings[inst[1]] = inst[2]
      types[inst[1]] = 'STRING'
    case 'MODULE':
      types[inst[1]] = 'MODULE'

    case 'MOV':
      aux_instructions.append(inst)
    case 'SUB':
      aux_instructions.append(inst)
    case 'ADD':
      aux_instructions.append(inst)
    case 'JEZ':
      aux_instructions.append(inst)
    case 'JNZ':
      aux_instructions.append(inst)
    case 'JGZ':
      aux_instructions.append(inst)
    case 'JLZ':
      aux_instructions.append(inst)
    case 'JMP':
      aux_instructions.append(inst)
    case 'LABEL':
      aux_instructions.append(inst)
      
  pass

def declare():
  global instructions
  for instruct in instructions:
    set_decalration(instruct)



def main():
  global instructions
  args = get_arguments()
  file = args[0]
  content = read_file(file)
  for i in range(0, len(content)):
    result = parser.parse(content[i])
    if (result != None):
      instructions.append(result)
  declare()

if __name__ == '__main__':
  main()