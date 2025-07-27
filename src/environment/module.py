from copy import copy

class MODULE_CORE:
  def __init__(self) -> None:
    self.acc = 0
    self.bak = 0
    self.next_inst = True
    self.inp = None
    self.out = None
    pass

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

  def get_inp(self) -> int:
    return self.inp

  def set_inp(self, new_input: int) -> bool:
    inserted = False
    if self.inp == None:
      inserted = True
      self.inp = new_input
    return inserted

  def retrieve_inp(self):
    inp = copy(self.inp)
    if self.inp != None:
      self.next_inst = True
      self.inp = None
    return inp
# TODO: pausar la ejecucion del modulo cuando se intenta poner un numero al out y ya hay un numero en el
  def set_out(self, new_out: int):
    self.next_inst = False
    self.out = new_out

  def get_out(self):
    out = copy(self.out)

    if out != None:
      self.next_inst = True
      self.inp = None

    return out

  def swp(self):
    aux = self.acc
    self.acc = self.bak
    self.bak = aux

class MODULE_CONTROLLER(MODULE_CORE):
  def __init__(self, instructions = []):
    super().__init__()
    self.instructions = instructions
    self.step = 0
    self.labels = {}

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

  def __mov_instruction(self, instruction: tuple):
    print(instruction)
    inst_p2 = instruction[1]
    inst_p3 = instruction[2]
    src = 0
    # get source
    match inst_p2:
      case 'INU':
        src = int(input('input:'))
      case 'ACC':
        src = self.acc
      case _:
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
        self.acc += self.acc
      case _:
        self.acc += int(inst_p2)

  def __sub_instruction(self, instruction: tuple):
    inst_p2 = instruction[1]

    match inst_p2:
      case 'ACC':
        self.acc -= self.acc
      case _:
        self.acc -= int(inst_p2)

  def execute_instruction(self):
    inst = self.instructions[self.step]

    inst_p1 = inst[0]
    match inst_p1:
      case 'MOV':
        self.__mov_instruction(inst)
      case 'ADD':
        self.__add_instruction(inst)
      case 'SUB':
        self.__sub_instruction(inst)

