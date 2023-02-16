import ply.yacc as yacc

from interpreter.lexer_asmm import tokens

current_module = None

start = 'start'

def p_start(p):
  'start :'

def p_inst_mov_acc_name(p):
  'sentence : MOV ACC NAME'
  p[0] = (p[1], p[2], p[3])

def p_inst_mov_num_acc(p):
  'sentence : MOV NUMBER ACC;'
  p[0] = (p[1], p[2], p[3])

def p_new_module(p):
  'sentence : MODULE NAME MOD_BEGIN'
  global current_module
  if(current_module != None):
    current_module = p[2]
    p[0] = ('MODULE', 'BEGIN', p[2])
  else:
    print('error: missing Token } ')
    exit(1)

def p_end_module(p):
  'sentence : MOD_END'
  global current_module
  p[0] = ('MODULE', 'END', current_module)
  current_module = None

def p_string_declaration(p):
  'sentence : STRING NAME EQUALS NAME_ALT END_INST'
  p[0] = ("STRING",p[2], p[4])

def p_vacio(p):
  'sentence : '
  pass

def p_error(p):
  print(p)
  print("Syntax error in line: %s" % p.lineno)
  print("token %s" % p.type)
  print("value "+ p.value)



parser = yacc.yacc()
