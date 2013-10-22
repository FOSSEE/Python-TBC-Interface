from sympy import *
import sys


print "Enter a function: ",
func = raw_input()

try:
    sym_x = Symbol('x')
    fx = S(func)
    fdashx = diff(fx, Symbol('x'))
except:
    print "Function could not be differenciated..."
    sys.exit()

print "Enter initial guess: ",
curr_root = float(raw_input())
print "Enter precision value: ",
precision = float(raw_input())
new_root = (curr_root - fx.subs({sym_x : curr_root})/fdashx.subs({sym_x : curr_root}))


iterations = 1
while(abs(new_root-curr_root)>precision):
    curr_root = new_root
    new_root = (curr_root - fx.subs({sym_x : curr_root})/fdashx.subs({sym_x : curr_root}))
    iterations += 1
    if iterations >= 50:
        print "Root was not derived uptil 50 iterations, current root: ", curr_root
        break

print "Function: ", fx
print "Given tolerance: ", precision
print "Number of iterations: ", iterations
print "Root to the funtion upto given precision: ", curr_root
