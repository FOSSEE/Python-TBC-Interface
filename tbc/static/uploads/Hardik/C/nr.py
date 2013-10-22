import sys, math, argparse, time
from sympy import *
 
start_time = time.time()
 
# using argparse to get command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--function", help = "Define a function")
parser.add_argument("-s", "--starting", help = "Starting point value", type = float, default = 0.0)
parser.add_argument("-p", "--precision", help = "Convergence precision", type = float, default = 5*10**(-6))
args = parser.parse_args()
 
sym_x = Symbol('x')
# convert the given function to a symbolic expression
try:
  fx = S(args.function)
except:
  sys.exit('Unable to convert function to symbolic expression.')
 
# calculate the differential of the function
try:
  dfdx = diff(fx, Symbol('x'))
except:
  sys.exit('Unable to differentiate function.')
 
# e is the relative error between 2 consecutive estimations of the root
e = 1
x0 = args.starting
iterations = 0
 
while ( e > args.precision ):
  # new root estimation
  try:   
    r = x0 - fx.subs({sym_x : x0})/dfdx.subs({sym_x : x0})
  except ZeroDivisionError:
    print "Function derivative is zero. Division by zero, program will terminate."
    sys.exit()
  # relative error
  e = abs((r - x0)/r)
  iterations += 1
  x0 = r
 
total_time = time.time() - start_time
 
print 'Function:'
pprint(fx)
print 'Derivative:'
pprint(dfdx)
print 'Root %10.6f calculated after %d iterations'%(r, iterations)
print 'Function value at root %10.6f'%(fx.subs({sym_x : r}),)
print 'Finished in %10.6f seconds'%(total_time,)
