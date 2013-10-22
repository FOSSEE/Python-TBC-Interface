import math             # Need to import math to use the log function
from Tkinter import *
import ttk
import tkMessageBox
import tkFileDialog
import os
import sys
# Variables that should be noted
# G = Guess value
# count = f(x)
# den = f'(x)
# Acc = Accuracy input from user

def CheckVals():
# Define variables as floats - decimal places
    r = 1
    if r == 1:
        try:                            #If any of the variables have errors catch
            G = float(GuessInp.get())
            A = float(AInp.get())
            B = float(BInp.get())
            Precision = int(AccInp.get())
            r = 0
            CalcRoot()
        except ValueError:
            tkinter.messagebox.showinfo("Look carefully","Oops, a variable isn't properly set")
            r = 0
    
    return
            
def CalcRoot():
    # Start the while loop
    G = float(GuessInp.get())
    A = float(AInp.get())
    B = float(BInp.get())
    Precision = int(AccInp.get())
    Acc = math.pow(0.1,Precision)

    count = Acc+1   # Just so we can get into the while loop (count > Acc)
    while count > Acc :
        count = (G*(math.log(A*G)))
        count = count - B
        if count > Acc:
            
            if count*A < 0: #Value not allowed
                tkinter.messagebox.showinfo("Look carefully","Calculations will become unstable Pi * a <0")
                return
            
##            if ((math.pow(math.exp(1),-1)/A)*count): #This seems like one of the prerequisites not sure if there is a typing error on the tut
##                tkinter.messagebox.showinfo("Look carefully","Calculations will become unstable Pi((e^-1)/a)")
##                return
            
            #Actual calculation
            den =(math.log(A*G))     #This is the derivtive denominator
            den = den + 1
            numb = count/den
            Temp = G - numb          #Guess value minus the calculated numb
            G = Temp
            count = (G*(math.log(A*G)))
            count = count - B
            
    button1.pack_forget()           #Hide Calculate button after success
    GText = StringVar()
    GText.set("Calculated Root: ")
    label1 = Label(app, textvariable=GText, height = 4)
    label1.pack()
    Roottxt = StringVar(None)
    Roottxt.set(G)   
    label7 = Label(app, textvariable=Roottxt)
    label7.pack()
    return


app = Tk()
app.title ("Newton Raphson approximation")
app.geometry('340x550+100+100')

CommText = StringVar()
CommText.set("Please complete the form and then click calculate")
label1 = Label(app, textvariable=CommText, height = 4)
label1.pack()

fxtxt = StringVar()
fxtxt.set("f(x) = (x * Ln(x * a)) - b\nf'(x) = 1 + Ln(ax)")
label2 = Label(app, textvariable=fxtxt, height = 4)
label2.pack()

#Input a
Atxt = StringVar()
Atxt.set("a = ")
label3 = Label(app, textvariable=Atxt, height = 2)
label3.pack()

A = StringVar(None)
AInp = Entry(app, textvariable=A)
AInp.pack()

#Input b
Btxt = StringVar()
Btxt.set("b = ")
label4 = Label(app, textvariable=Btxt, height = 2)
label4.pack()

B = StringVar(None)
BInp = Entry(app, textvariable=B)
BInp.pack()

#Input acc
DegText = StringVar()
DegText.set("To what accuracy do you want the root: ")
label5 = Label(app, textvariable=DegText, height = 4)
label5.pack()

Acc = StringVar(None)
AccInp = Entry(app, textvariable=Acc)
AccInp.pack()

#Input guess
Guesstxt = StringVar()
Guesstxt.set("What is your guess of the root")
label6 = Label(app, textvariable=Guesstxt, height = 4)
label6.pack()

G = StringVar(None)
GuessInp = Entry(app, textvariable=G)
GuessInp.pack()

#Calculation button
button1 = Button(app, text = "Calculate root", width = 20, command = CheckVals)
button1.pack(padx = 15,pady = 15)

app.mainloop() 
