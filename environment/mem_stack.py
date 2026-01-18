class MEM_STACK():
  mem: list[str]

  def __init__(self) -> None:
    self.mem = []

  def get_a_value(self) -> int | None:
    try:
      return self.mem.pop()
    except IndexError:
      return None

  def send_a_value(self, new_value:int) -> None:
    self.mem.append(new_value)

  def get_state(self) -> dict:
    return {
      'mem': self.mem 
    }
