from threading import Thread

class MODULE():
  def __init__(self, name:str, instructions = []) -> None:
    self.acc = 0
    self.bak = 0
    self.inst = 0
    self.instructions = instructions
    self.thr = Thread(target=self.execute_module, name=name)
    pass

  def add(self, number:int):
    self.acc += number

  def sub(self, number:int):
    self.acc -= number

  def sav(self):
    self.bak = self.acc

  def swp(self):
    aux = self.acc
    self.acc = self.bak
    self.bak = aux

  def execute_module(self):
    while True:
      self.next_instruction()

  def next_instruction(self):
    

    self.inst += 1
    if(self.inst > len(self.instructions)):
      self.inst = 0