import math
import numpy as np
import pl

#constantes
PRECISION_DECIMAL = 6
PRECISION = 10e-6
PRINT_PRECISION = 7

def get_PL():
  #get pl size
  rest_num, var_num = input().split()

  #get max value
  vector_c = convert_list_to_int(input().split())
  restrictions = []
  vector_b = []

  #get restrictions and vector b
  for i in range(int(rest_num)):
    line = input().split()
    line = convert_list_to_int(line)
    restrictions.append(line[:int(var_num)])
    vector_b.append(int(line[-1]))
  
  return pl.PL(int(rest_num), int(var_num), restrictions, vector_c, vector_b)

def convert_list_to_int(list):
  for i in range(len(list)):
    list[i] = int(list[i])
  return list

def postive_b_vector(tableau):
  for i in range(1, tableau.shape[0]):
    if(tableau[i][-1] < 0):
      tableau[i] = - tableau[i]
  return tableau

def is_viable(tableau):
  if is_almost_equal(tableau[0][-1],0): return True
  else: False

def is_almost_equal(a,b):
  return abs(a - b) < PRECISION

#pivoting
def pivot_column(tableau, y_pivot, x_pivot):
  pivot = tableau[y_pivot][x_pivot]
  print(f"😗 Pivoteando os elementos = {y_pivot}, {x_pivot}")
  print(f"Valor do pivo = {pivot}")
  print(f"Valor do pivo = {pivot}")
  print(tableau)
  tableau[y_pivot] = (1/pivot)*(tableau[y_pivot])
  for i in range(y_pivot):
    zerable = tableau[i][x_pivot]
    tableau[i] = tableau[i] - zerable * tableau[y_pivot]
    tableau[i][x_pivot] = 0 #zerando a coluna em cima do pivo
  for i in range(y_pivot + 1, tableau.shape[0]):
    zerable = tableau[i][x_pivot]
    tableau[i] = tableau[i] - zerable * tableau[y_pivot]
    tableau[i][x_pivot] = 0 #zerando a coluna abaixo do pivo
  return(tableau)

def define_pivot(tableau, column):
  pivot = 1;
  pivot_ratio = math.inf
  unlimited_state = 'i'
  for i in range(1, tableau.shape[0]):
    # maquina de estados se é ilimitada
    if tableau[i][column] <= PRECISION:
      continue
      
    if tableau[i][-1]/tableau[i][column] <= pivot_ratio:
      pivot = i
      pivot_ratio = tableau[i][-1]/tableau[i][column]
      unlimited_state = 'l'
  if unlimited_state == 'i': pivot = -1
  return(pivot)


def print_list(list):
  for i in range(list.size-1):
    print("{:.7f}".format(round(list[i], PRINT_PRECISION)),end = ' ')
  print("{:.7f}".format(round(list[list.size-1], PRINT_PRECISION)))
