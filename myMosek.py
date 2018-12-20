import numpy as np
from numpy import array, zeros, ones
import mosek
import sys
from readModule import readSpots
from SpotMatrix import SpotMatrix

data, shifts = readSpots()
SM = SpotMatrix(np.array(data), np.array(shifts))

def streamprinter(text):
    sys.stdout.write(text)
    sys.stdout.flush()

def mosek_solution ():
    # Make a MOSEK environment
    env = mosek.Env ()
    # Attach a printer to the environment
    env.set_Stream (mosek.streamtype.log, streamprinter)
  
    # Create a task
    task = env.Task(0,0)
    # Attach a printer to the task
    task.set_Stream (mosek.streamtype.log, streamprinter)
  
    numvar = len(SM.toVector())
    numcon = SM.columnCount()

    bkc = [mosek.boundkey.ra] * numcon #constraints
    blc = zeros(numcon)
    buc = ones(numcon)

    bkx = [ mosek.boundkey.ra] * numvar #variables
    blx = zeros(numvar)
    bux = ones(numvar)

    c   = SM.toVector()

    asub, aval = SM.indicators()

    # Append 'numcon' empty constraints.
    # The constraints will initially have no bounds. 
    task.appendcons(numcon)
     
    # Append 'numvar' variables.
    # The variables will initially be fixed at zero (x=0). 
    task.appendvars(numvar)

    for j in range(numvar):
        # Set the linear term c_j in the objective.
        task.putcj(j,c[j])
        # Set the bounds on variable j
        # blx[j] <= x_j <= bux[j] 
        task.putvarbound(j,bkx[j],blx[j],bux[j])
        # Input column j of A 
        task.putacol(j,                  # Variable (column) index.
                 asub[j],            # Row index of non-zeros in column j.
                 aval[j])            # Non-zero Values of column j. 

    task.putconboundlist(range(numcon),bkc,blc,buc)
        
    # Input the objective sense (minimize/maximize)
    task.putobjsense(mosek.objsense.maximize)
       
    # Define variables to be integers
    task.putvartypelist([x for x in range(numvar)],
                        [ mosek.variabletype.type_int] * numvar)
        
    # Optimize the task
    task.optimize()

    # Print a summary containing information
    # about the solution for debugging purposes
    task.solutionsummary(mosek.streamtype.msg)

    prosta = task.getprosta(mosek.soltype.itg)
    solsta = task.getsolsta(mosek.soltype.itg)

    # X

    # Output a solution
    xx = zeros(numvar, float)
    task.getxx(mosek.soltype.itg,xx)

    print(mosek.solsta.integer_optimal)

    # if solsta in [ mosek.solsta.integer_optimal, mosek.solsta.near_integer_optimal ]:
    #     print("Optimal solution: %s" % xx)
    # elif solsta == mosek.solsta.dual_infeas_cer: 
    #     print("Primal or dual infeasibility.\n")
    # elif solsta == mosek.solsta.prim_infeas_cer:
    #     print("Primal or dual infeasibility.\n")
    # elif solsta == mosek.solsta.near_dual_infeas_cer:
    #     print("Primal or dual infeasibility.\n")
    # elif  solsta == mosek.solsta.near_prim_infeas_cer:
    #     print("Primal or dual infeasibility.\n")
    # elif mosek.solsta.unknown:
    #     if prosta == mosek.prosta.prim_infeas_or_unbounded:
    #         print("Problem status Infeasible or unbounded.\n")
    #     elif prosta == mosek.prosta.prim_infeas:
    #         print("Problem status Infeasible.\n")
    #     elif prosta == mosek.prosta.unkown:
    #         print("Problem status unkown.\n")
    #     else:
    #         print("Other problem status.\n")
    # else:
    #     print("Other solution status")