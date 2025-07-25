import ply.yacc as yacc
from interpreter.lexer_asmm import tokens

current_module = None

def p_inst_label(p):
  'sentence : LABEL'
  p[0] = ('LABEL', p[1])

def p_inst_swp(p):
  'sentence : SWP'
  p[0] = ('SWP')

def p_inst_sub_num(p):
  'sentence : SUB NUMBER END_INST'
  p[0] = ('SUB', p[1])

def p_inst_sub_acc(p):
  'sentence : SUB ACC END_INST'
  p[0] = ('SUB', 'ACC')

def p_inst_add_num(p):
  'sentence : ADD NUMBER END_INST'
  p[0] = ('ADD', p[1])

def p_inst_add_acc(p):
  'sentence : ADD ACC END_INST'
  p[0] = ('ADD', 'ACC')

def p_inst_mov_acc_name(p):
  'sentence : MOV ACC NAME END_INST'
  p[0] = (p[1], p[2], p[3])

def p_inst_mov_num_acc(p):
  'sentence : MOV NUMBER ACC END_INST'
  p[0] = (p[1], p[2], p[3])

def p_inst_mov_in_acc(p):
  'sentence : MOV IN ACC END_INST'
  p[0] = (p[1], p[2], p[3])
  
def p_inst_mov_inu_acc(p):
  'sentence : MOV IN_USER ACC END_INST'
  p[0] = (p[1], p[2], p[3])

def p_inst_mov_acc_out(p):
  'sentence : MOV ACC OUT END_INST'
  p[0] = ('MOV', 'ACC', 'OUT')

def p_inst_mov_acc_outp(p):
  'sentence : MOV ACC OUT_SCREEN END_INST'
  p[0] = ('MOV', 'ACC', 'OUTP')

def p_inst_jnz(p):
  'sentence : JNZ NAME END_INST'
  p[0] = ('JNZ', p[2])

def p_inst_jez(p):
  'sentence : JEZ NAME END_INST'
  p[0] = ('JEZ', p[2])

def p_new_module(p):
  'sentence : MODULE NAME MOD_BEGIN'
  global current_module
  if(current_module == None):
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
  exit(1)



parser = yacc.yacc()
