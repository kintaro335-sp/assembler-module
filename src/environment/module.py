class MODULE_CORE:
  def __init__(self) -> None:
    self.acc = 0
    self.bak = 0
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

  def set_out(self, new_out: int):
    self.out = new_out

  def get_out(self):
    return self.out

  def swp(self):
    aux = self.acc
    self.acc = self.bak
    self.bak = aux

class MODULE_CONTROLLER(MODULE_CORE):
  def __init__(self, instructions = []):
    super().__init__()
  # TODO: add instrction loader and the executer
