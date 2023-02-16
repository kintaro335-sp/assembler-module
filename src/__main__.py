from utils.arguments import get_arguments
from utils.files_utils import read_file
from interpreter.parser import parser

def main():
  global line_num
  args = get_arguments()
  file = args[0]
  content = read_file(file)
  print('result')
  
  result = parser.parse(content)
  print(result)
  pass

if __name__ == '__main__':
  main()