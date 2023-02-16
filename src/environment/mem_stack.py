class MEM_STACK():
  def __init__(self) -> None:
    self.mem = [0,0,0,0,0,0,0,0,0,0]
    self.pointer = 0

  def get_a_value(self) -> int:
    aux = self.pointer
    self.pointer =+ 1
    return self.mem[aux]

  def set_a_value(self, new_value:int) -> None:
    self.mem[self.pointer] = new_value
    self.pointer =+ 1

  def set_pointer(self, new_pointer: int) -> None:
    self.pointer = new_pointer
