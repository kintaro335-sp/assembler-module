

def read_file(name: str):
  file = open(name, 'r')
  lines = file.readlines()
  content = ''
  for line in lines:
    content += line + '\n'
  return content
