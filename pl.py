from traceback import print_tb
import numpy as np
import aux_functions as aux

np.set_printoptions(precision=2, linewidth=200, suppress=True)

class PL:
  def __init__(self, rest_num, var_num, A, c_vector, b_vector):
      self.rest_num = rest_num
      self.var_num = var_num
      self.fpi_size = var_num + rest_num
      self.A_matrix = np.array(A)
      self.c_vector = np.array(c_vector)
      self.b_vector = np.array(b_vector)
      self.tableau = self.create_tableau()
      self.aux_tableau = self.create_aux()

  def create_tableau(self):
    tableau_bottom = np.concatenate((np.identity(self.rest_num), self.A_matrix, np.identity(self.rest_num), np.expand_dims(self.b_vector, axis=1)), axis = 1)
    tableau_top = np.concatenate((np.zeros(self.rest_num), - self.c_vector, np.zeros(self.rest_num + 1)))
    tableau = np.concatenate((np.expand_dims(tableau_top, axis=0), tableau_bottom), axis = 0)
    return aux.postive_b_vector(tableau)
  
  def create_aux(self):
    tableau_bottom = np.concatenate((self.tableau[1:,0:-1], np.identity(self.rest_num), np.expand_dims(self.tableau[1:,-1], axis=1)), axis = 1)
    tableau_top = np.concatenate((np.zeros(self.rest_num + self.fpi_size), np.ones(self.rest_num), np.zeros(1)))
    tableau_top = tableau_top - np.sum(tableau_bottom, axis=0)
    tableau = np.concatenate((np.expand_dims(tableau_top, axis=0), tableau_bottom), axis = 0)
    return(tableau)
  
  def next_column_to_optimize(self, mode):
    tableau = self.aux_tableau if mode == "aux" else self.tableau
    size_max = 2 * self.rest_num + self.fpi_size if mode == "aux" else self.fpi_size + self.rest_num
    
    for i in range(self.rest_num, size_max):
      if(tableau[0][i] < -aux.PRECISION): 
          return i
    return -1

  def aux_simplex(self):
    next = self.next_column_to_optimize("aux")
    tableau = self.aux_tableau
    bases = []
    while(next > 0):
      pivot = aux.define_pivot(tableau, next)
      tableau = aux.pivot_column(tableau, pivot, next)
      bases = list(filter(lambda c: c[0] != pivot, bases))
      bases.append((pivot, next))
      next = self.next_column_to_optimize("aux")
    else: return (bases, tableau)

  def get_first_canonical_primal(self, base, tableau):
    for i in base:
      pivot = aux.define_pivot(tableau, i[1])
      tableau = aux.pivot_column(tableau, pivot, i[1])
    return tableau

  def primal_simplex(self, bases):
    next = self.next_column_to_optimize("primal")
    #converte tableau para canonica
    tableau = self.get_first_canonical_primal(bases, self.tableau)
    #itera colunas negativas
    while(next > 0):
      pivot = aux.define_pivot(tableau, next)
      if pivot == -1: return ("ilimitado", bases, tableau, next)
      tableau = aux.pivot_column(tableau, pivot, next)
      bases = list(filter(lambda c: c[0] != pivot, bases))
      bases.append((pivot, next))
      next = self.next_column_to_optimize("prim")

    else: return ("viavel", bases, tableau, next)

  def result_analyze(self, bases, tableau):
    if not aux.is_viable(tableau):
        print("inviavel")
        aux.print_list(tableau[0, 0:self.rest_num])
    else:
      primal = self.primal_simplex(bases)
      if primal[0] == "ilimitado":
        print("ilimitada")
        aux.print_list(self.get_viable_solution(primal[1], primal[2]))
        aux.print_list(self.get_unlimited_certificate(primal[3], bases, primal[2]))
      else:
        print("otima")
        print("{:.7f}".format(round(primal[2][0,-1], aux.PRINT_PRECISION)))
        aux.print_list(self.get_viable_solution(primal[1], primal[2]))
        aux.print_list(primal[2][0,0:self.rest_num])


  def get_unlimited_certificate(self, unlimited_col, bases, tableau):
    cert = np.zeros(self.fpi_size)
    cert[unlimited_col - self.rest_num] = 1
    for i in bases:
      cert[i[1] - self.rest_num] = - tableau[i[0], unlimited_col]
    return cert[0:self.var_num]
  
  def get_viable_solution(self, base, tableau):
    solution = np.zeros(self.fpi_size)
    for i in base:
        solution[i[1] - self.rest_num] = tableau[i[0], -1]
    return solution[0:self.var_num]
