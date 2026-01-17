import os
from typing import Tuple, Literal
from copy import copy
from .module import MODULE_CONTROLLER
from .mem_stack import MEM_STACK


class Machine:
  mode: Literal['DEFAULT', 'WEB']
  modules: dict[str, MODULE_CONTROLLER] = {}
  mem_stacks: dict[str, MEM_STACK] = {}
  types: dict[str, Literal['MODULE', 'MEM']]
  strings: dict[str, str] = {}
  ticks: int = 0
  cycle_executed = False

  def __init__(self, instructions:list[Tuple] = [], mode: Literal['DEFAULT', 'WEB'] = 'DEFAULT'):
    self.instructions = instructions
    self.ticks = 0
    self.strings = {}
    self.mem_stacks = {}
    self.modules = {}
    self.types = {}
    self.cycle_executed = False
    self.mode = mode
    self.__initialize()

  def __initialize_module(self, name: str, start_module: int, end_module: int):
    i = start_module
    instrections_module: list[Tuple] = []
    while i <= end_module:
      instrections_module.append(self.instructions[i])
      i += 1
    self.modules[name] = MODULE_CONTROLLER(instrections_module, self.mode)

  def __define_type(self, name: str, type_e: Literal['MODULE', 'MEM']):
    type_name = self.types.get(name)
    if type_name == None:
      self.types[name] = type_e
    else:
      print('Error: names duplicated')
      os._exit(1)

  def __initialize(self):

    for i, inst in enumerate(self.instructions):
      match inst[0]:
        case 'STRING':
          self.strings[inst[1]] = inst[2]
        case 'MODULE':
          if inst[1] == 'BEGIN':
            module_name = inst[2]
            self.__define_type(module_name, 'MODULE')
            end_inst = copy(i)
            while self.instructions[end_inst][1] != 'END':
              end_inst += 1
            self.__initialize_module(inst[2], i + 1, end_inst - 1)
          elif inst[1] == 'END':
            print(f'module end declaration:{module_name}')
        case 'MEM':
          self.mem_stacks[inst[1]] = MEM_STACK()
          self.__define_type(inst[1], 'MEM')

  def __send_value_to_mem_stack(self, origin: str, destination: str):
      mov_ints_origin = self.modules[origin].get_current_instruction()
      src_mov_inst = mov_ints_origin[1]
      src = 0
      match src_mov_inst:
        case 'ACC':
          src = self.modules[origin].get_acc()
        case _:
          src = src_mov_inst
      self.mem_stacks[destination].send_a_value(src)

  def __send_value_to_module(self, origin: str, destination: str):
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
      inserted = self.modules[destination].set_inp(origin, src)
      if not inserted:
        # No se que agregar aqui
        pass
        # self.modules[origin].pause()
    else:
      self.modules[origin].pause()

  def __retrive_from_mem_stack(self, origin: str, destination: str):
    num_retrieved = self.mem_stacks[origin].get_a_value()
    if num_retrieved != None:
      inserted = self.modules[destination].set_inp(origin, num_retrieved)
  
  def set_input(self, new_input:int):
    modules_keys = self.modules.keys()
    for mod_key in modules_keys:
      if self.modules[mod_key].required_input():
        self.modules[mod_key].set_input_ext(new_input)

  def set_input_to_module(self, module: str, new_input: int):
    module = self.modules.get(module)
    if module != None:
      self.modules[module].set_input_ext(new_input)

  def get_required_inputs(self) -> list[str]:
    module_list = []
    modules_keys = self.modules.keys()

    for mod_key in modules_keys:
      if self.modules[mod_key].required_input():
        module_list.append(mod_key)

    return module_list

  def execute_instructions(self):
    if self.mode == "WEB":
      if len(self.get_required_inputs()) > 0:
        return
    if self.cycle_executed:
      return
    modules_keys = self.modules.keys()
    for key in modules_keys:
      current_instruction = self.modules[key].get_current_instruction()
      inst_p1 = current_instruction[0]
      match inst_p1:
        case 'PRINT':
          string = self.strings.get(current_instruction[1])
          print(string)
        case 'MOV':
          inst_p2 = current_instruction[1]
          type_origin = self.types.get(inst_p2)
          inst_p3 = current_instruction[2]
          module_dest = self.types.get(inst_p3)
          if type_origin == 'MODULE' or inst_p2 == 'ACC':
            match module_dest:
              case 'MODULE':
                self.__send_value_to_module(key, inst_p3)
              case 'MEM':
                self.__send_value_to_mem_stack(key, inst_p3)
          elif type_origin == 'MEM':
            self.__retrive_from_mem_stack(inst_p2, key)
        case 'ADD':
          inst_p2 = current_instruction[1]
          type_origin = self.types.get(inst_p2)
          if type_origin == 'MEM':
            self.__retrive_from_mem_stack(inst_p2, key)
        case 'SUB':
          inst_p2 = current_instruction[1]
          type_origin = self.types.get(inst_p2)
          if type_origin == 'MEM':
            self.__retrive_from_mem_stack(inst_p2, key)
          
      self.modules[key].execute_instruction()
    self.cycle_executed = True

  def next_tick(self):
    if not self.cycle_executed:
      return
    self.ticks += 1
    modules_keys = self.modules.keys()
    for key in modules_keys:
      self.modules[key].next_instruction()
    self.cycle_executed = False

  def get_state(self) -> dict:
    state = {
      'executed': self.cycle_executed,
      'tick': self.ticks,
    }
    # modules state
    modules_state = {}
    modules_keys = self.modules.keys()
    for mod_key in modules_keys:
      modules_state[mod_key] = self.modules[mod_key].get_state()
    state['modules'] = modules_state

    # memory stacks
    mem_stacks_state = {}
    mem_stacks_keys = self.mem_stacks.keys()
    for mem_key in mem_stacks_keys:
      mem_stacks_state[mem_key] = self.mem_stacks[mem_key].get_state()
    state['mem_stacks'] = mem_stacks_state

    return state
