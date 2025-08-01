import ply.lex as lex

literals = [';']

tokens = (
  'ACC',
  'ADD',
  'JEZ',
  'JMP',
  'JGZ',
  'JLZ',
  'JNZ',
  'LABEL',
  'NAME',
  'NEG',
  'NUMBER',
  'MEM',
  'MODULE',
  'MOV',
  'OUT_SCREEN',
  'OUT',
  'IN',
  'IN_USER',
  'SUB',
  'STRING',
  'SWP',
  'SAV',
  'MOD_BEGIN',
  'MOD_END',
  'NAME_ALT',
  'EQUALS',
  'END_INST',
  'HALT'
)

t_EQUALS = r'='

t_END_INST = r';'

t_IN_USER = r'INU'

t_ignore = ' \t'

t_HALT = r'HALT'

def t_NAME_ALT(t):
  r'"[a-zA-Z0-9_\s]+"'
  t.value = str(t.value).replace('"', '')
  return t

t_ACC = r'ACC'

t_ADD = r'ADD'

def t_LABEL(t):
  r'[a-z]+:'
  return t

def t_NAME(t):
  r'[a-z_]+'
  t.value = str(t.value)
  return t

t_NEG = r'NEG'

def t_NUMBER(t):
  r'[0-9]+'
  t.value = int(t.value)
  return t

t_MEM = r'MEM'

t_MODULE = r'MODULE'

t_IN = r'IN'

t_MOD_BEGIN = r'{'

t_MOD_END = r'}'

t_MOV = r'MOV'

t_OUT_SCREEN = r'OUTP'

t_OUT = r'OUT' 

t_SUB = r'SUB'

t_SWP = r'SPW'

t_SAV = r'SAV'

t_STRING = r'STRING'

t_JNZ = r'JNZ'

t_JEZ = r'JEZ'

t_JGZ = r'JGZ'

t_JLZ = r'JLZ'

t_JMP = r'JMP'

def t_newline(t):
  r'\n'
  t.lexer.lineno += len(t.value)

def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)

lexer = lex.lex()
