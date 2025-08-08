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

  def __initialize_module(self, name: str, start_module: int, end_module: int):
    i = start_module
    instrections_module: list[Tuple] = []
    while i <= end_module:
      instrections_module.append(self.instructions[i])
      i += 1
    self.modules[name] = MODULE_CONTROLLER(instrections_module)

  def __initialize(self):

    for i, inst in enumerate(self.instructions):
      match inst[0]:
        case 'STRING':
          self.strings[inst[1]] = inst[2]
        case 'MODULE':
          if inst[1] == 'BEGIN':
            module_name = inst[2]
            end_inst = copy(i)
            while self.instructions[end_inst][1] != 'END':
              end_inst += 1
            self.__initialize_module(inst[2], i + 1, end_inst - 1)
          elif inst[1] == 'END':
            print(f'module end declaration:{module_name}')
        case 'MEM':
          self.mem_stacks[inst[1]] = MEM_STACK()

  def send_value_to_module(self, origin: str, destination: str):
    inp_dest = self.modules[destination].get_inp(origin)
    if inp_dest == None:
      mov_ints_origin = self.modules[origin].get_current_instruction()
      src_mov_inst = mov_ints_origin[1]
      src = 0
      match src_mov_inst:
        case 'ACC':
          src = self.modules[origin].get_acc()
        case _:
          src = src_mov_inst
      self.modules[destination].set_inp(origin, src)
    else:
      self.modules[origin].pause()
    
  def execute_instructions(self):
    modules_keys = self.modules.keys()
    for key in modules_keys:
      current_instruction = self.modules[key].get_current_instruction()
      inst_p1 = current_instruction[0]
      if inst_p1 == 'MOV':
        inst_p3 = current_instruction[2]
        module_dest = self.modules.get(inst_p3)
        if module_dest != None:
          self.send_value_to_module(key, inst_p3)
      self.modules[key].execute_instruction()

  def next_tick(self):
    self.ticks += 1
    modules_keys = self.modules.keys()
    for key in modules_keys:
      self.modules[key].next_instruction()

