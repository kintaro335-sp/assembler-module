from utils.arguments import get_arguments
from utils.files_utils import read_file
from interpreter.parser import parser

declaration = []

def main():
  global declaration
  args = get_arguments()
  file = args[0]
  content = read_file(file)
  for i in range(0, len(content)):
    result = parser.parse(content[i])
    if (result != None):
      declaration.append(result)
    print(i)
  print(declaration)
  pass

if __name__ == '__main__':
  main()