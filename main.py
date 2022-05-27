import pl
import aux_functions as aux

def main():
    print("Digita carai")
    pl_obj = aux.get_PL();
    aux_solved_pl = pl_obj.aux_simplex()
    analyze = pl_obj.result_analyze(*aux_solved_pl)

main()
