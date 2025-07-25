from typing import Tuple
from copy import copy
from .module import MODULE_CONTROLLER
from .mem_stack import MEM_STACK


class Machine:
  modules: dict[str, MODULE_CONTROLLER] = {}
  mem_stacks: dict[str, MEM_STACK] = {}
  strings: dict[str, str] = {}
  ticks: int = 0

  def __init__(self, instructions:list[Tuple] = []):
    self.instructions = instructions
    self.ticks = 0
    self.strings = {}
    self.mem_stacks = {}
    self.modules = {}
    self.__initialize()

  def __initialize_module(self, start_module: int, end_module: int):
    i = start_module
    instrections_module: list[Tuple] = []
    while i <= end_module:
      instrections_module.append(self.instructions[i])
      i += 1
    self.modules[self.instructions[start_module][1]] = MODULE_CONTROLLER(instrections_module)

  def __initialize(self):

    for i, inst in enumerate(self.instructions):
      match inst[0]:
        case 'STRING':
          self.strings[inst[1]] = inst[2]
        case 'MODULE':
          if inst[1] == 'BEGIN':
            end_inst = copy(i)
            while self.instructions[end_inst][1] != 'END':
              end_inst += 1
            self.__initialize_module(i + 1, end_inst - 1)
        case 'MEM':
          self.mem_stacks[inst[1]] = MEM_STACK()

    
  def execute_instructions(self):
    modules_keys = self.modules.keys()
    for key in modules_keys:
      self.modules[key].execute_instruction()

  def next_tick(self):
    self.ticks += 1
    modules_keys = self.modules.keys()
    for key in modules_keys:
      self.modules[key].next_instruction()

