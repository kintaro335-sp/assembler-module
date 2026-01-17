import os
from typing import Literal
from utils.eval import eval_value
from copy import copy

class MODULE_CORE:
  inp: dict[str, int]
  def __init__(self) -> None:
    self.acc = 0
    self.bak = 0
    self.next_inst = True
    self.inp = {}

  def add(self, number:int):
    self.acc += number

  def sub(self, number:int):
    self.acc -= number

  def sav(self):
    self.bak = self.acc

  def get_acc(self):
    return self.acc

  def set_acc(self, new_acc_value: int):
    self.acc = new_acc_value

  def get_inp(self, sender: str) -> int | None:
    return self.inp.get(sender)

  def set_inp(self, sender: str, new_input: int) -> bool:
    inserted = False
    if self.inp.get(sender) == None:
      inserted = True
      self.inp[sender] = new_input
    return inserted

  def retrieve_inp(self, sender: str):
    inp = copy(self.inp.get(sender))
    if self.inp.get(sender) != None:
      self.next_inst = True
      del self.inp[sender]
    return inp

  def swp(self):
    aux = self.acc
    self.acc = self.bak
    self.bak = aux

class MODULE_CONTROLLER(MODULE_CORE):
  mode: Literal['DEAULT', 'WEB']
  instructions: list[tuple]
  step: int
  labels: dict
  input_ext: int | None
  def __init__(self, instructions: list[tuple] = [], mode:Literal['DEFAULT', 'WEB'] = 'DEFAULT'):
    super().__init__()
    self.instructions = instructions
    self.step = 0
    self.labels = {}
    self.inputs = {}
    self.mode = mode
    for i in range(0, len(self.instructions)):
      if self.instructions[i][0] == 'LABEL':
        self.labels[self.instructions[i][1]] = i

  def get_current_instruction(self) -> tuple:
    return self.instructions[self.step]

  def next_instruction(self):
    if not self.next_inst:
      return
    self.step += 1
    if self.step > len(self.instructions) - 1:
      self.step = 0

  def set_input_ext(self, new_val: int):
    self.input_ext = new_val

  def required_input(self) -> bool:
    inst = self.get_current_instruction()
    if inst[0] == 'MOV':
      return inst[1] == 'INU' and self.input_ext == None
    return False

  def pause(self):
    self.next_inst = False

  def __mov_instruction(self, instruction: tuple):
    inst_p2 = instruction[1]
    inst_p3 = instruction[2]
    src = 0
    # get source
    match inst_p2:
      case 'INU':
        src = self.__input()
      case 'ACC':
        src = self.acc
      case _:
        type_value = eval_value(inst_p2)
        match type_value:
          case 'NAME':
            src = self.get_inp(inst_p2)
            if src == None:
              self.next_inst = False
              return
            else:
              src = self.retrieve_inp(inst_p2)
          case 'NUMBER':
            src = inst_p2
    
    match inst_p3:
      case 'OUT':
        if self.out != None:
          self.out = src
          self.next_inst = False
      case 'OUTP':
        print(src)
      case 'ACC':
        self.acc = src

  def __add_instruction(self, instruction: tuple):
    inst_p2 = instruction[1]
    print(instruction)

    match inst_p2:
      case 'ACC':
        self.add(self.acc)
      case _:
        type_value = eval_value(inst_p2)
        match type_value:
          case 'NAME':
            print(f'inst {inst_p2}')
            if self.get_inp(inst_p2) != None:
              self.add(self.retrieve_inp(inst_p2))
            else:
              self.pause()
          case 'NUMBER':
            self.add(int(inst_p2))

  def __sub_instruction(self, instruction: tuple):
    inst_p2 = instruction[1]

    match inst_p2:
      case 'ACC':
        self.sub(self.acc)
      case _:
        type_value = eval_value(inst_p2)
        match type_value:
          case 'NAME':
            if self.get_inp() != None:
              self.add(self.retrieve_inp(inst_p2))
            else:
              self.pause()
          case 'NUMBER':
            self.sub(int(inst_p2))

  def __jez_instruction(self, inst: tuple):
    inst_p2 = inst[1]
    if self.acc == 0:
      self.step = self.labels[f"{inst_p2}:"]

  def __jnz_instruction(self, inst: tuple):
    inst_p2 = inst[1]
    if self.acc != 0:
      self.step = self.labels[f"{inst_p2}:"]

  def __jgz_instruction(self, inst: tuple):
    inst_p2 = inst[1]
    if self.acc > 0:
      self.step = self.labels[f"{inst_p2}:"]

  def __jlz_instruction(self, inst: tuple):
    inst_p2 = inst[1]
    if self.acc < 0:
      self.step = self.labels[f"{inst_p2}:"]

  def __jmp_instruction(self, inst: tuple):
    inst_p2 = inst[1]
    self.step = self.labels[f"{inst_p2}:"]

  def __input(self) -> int:
    if self.mode == 'WEB':
      input_num = copy(self.input_ext)
      self.input_ext = None
      return input_num
    while (True):
      try:
        return int(input('input:'))
      except ValueError:
        print('invalid input')


  def execute_instruction(self):
    print(f"step:{self.step}")
    inst = self.instructions[self.step]
    print(inst)
    inst_p1 = inst[0]
    match inst_p1:
      case 'MOV':
        self.__mov_instruction(inst)
      case 'ADD':
        self.__add_instruction(inst)
      case 'SUB':
        self.__sub_instruction(inst)
      case 'JEZ':
        self.__jez_instruction(inst)
      case 'JNZ':
        self.__jnz_instruction(inst)
      case 'JMP':
        self.__jmp_instruction(inst)
      case 'JGZ':
        self.__jgz_instruction(inst)
      case 'JLZ':
        self.__jlz_instruction(inst)
      case 'SAV':
        self.sav()
      case 'SWP':
        self.swp()
      case 'LABEL':
        pass
      case 'HALT':
        os._exit(0)

  def get_state(self):
    return {
      'instructions': self.instructions,
      'step': self.step,
      'acc': self.acc,
      'bak': self.bak,
      'req_input': self.required_input()
    }
