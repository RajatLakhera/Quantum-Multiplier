
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile, Aer, execute, IBMQ
from math import pi
#----------------------------------------------------------------------------------------------------------------------
'''This function operates on a quantum register and converts it from Computational to Fourier Basis for further addition.
In other words, it is creating Fourier Transform of the register which is basically a sequence of controlled pahse rotations'''

def QFT(circuit, quantum_register, n):              #why not use pi in the function directly?
    qc.h(quantum_register[n])
    for j in range (0,n):
        circuit.cp(pi/float(2**(j+1)), quantum_register[n - (j+1)], quantum_register[n])
#----------------------------------------------------------------------------------------------------------------------

'''This function performs Inverse Fourier Transform on the quantum register and converts the state back to computational basis'''

def Inverse_QFT(circuit,quantum_register, n):
    for j in range(0, n):
        circuit.cp(-1 * pi / float(2**(n - j)), quantum_register[j], quantum_register[n])
    circuit.h(quantum_register[n])
#---------------------------------------------------------------------------------------------------------------------

'''This function applies Fourier Transform on the combined state of register_x and register_y. Here register_y acts as controller
for rotations on register_x'''

def QFT_adder(circuit, register_x, register_y, n, factor):
    l = len(register_y)
    for j in range (0, n+1):
        if (n - j ) > l - 1:
            pass
        else:
            circuit.cp(factor*pi /  float(2**(j)),register_y[n - j], register_x[n])
#---------------------------------------------------------------------------------------------------------------------
#How to use the above function to subtract? => using value of factor as -1 instead of 1

'''Putting together all the above functions. Here the term factor is used to tell the program whether to add or to subrtract'''

def summation(register_x, register_y, qc, factor):
    n = len(register_x) - 1
    
    for i in range(0, n+1):
        QFT(qc, register_x, n-i)
    
    for i in range(0, n+1):
        QFT_adder(qc, register_x, register_y, n-i, factor)
    
    for i in range(0, n+1):
        Inverse_QFT(qc, register_x, i)
#--------------------------------------------------------------------------------------------------------------------

'''Taking inputs and creating the quantum circuit with required registers'''

#Taking the two numbers from user (decimal form)
multiplicand_string = input("Enter the value of multiplicand: ")
multiplier_string = input("Enter the value of multiplier: ")

#To let the user know that the program is running
print("Processing.....")

#Conversion of numbers from decimal to binary base
multiplicand_string = bin(int(multiplicand_string))
multiplier_string = bin(int(multiplier_string))

#The binary conversion above has terms "0b" in the beginning to indicate binary basis
#This would however interfere with program's working so the characters are deleted
multiplicand_string = multiplicand_string.replace('0b','')
multiplier_string = multiplier_string.replace('0b', '')

#finding lengths of the two numbers
n1 = len(multiplicand_string)
n2 = len(multiplier_string)
n = n1 + n2

#To reduce the number of iterations and optimize the circuit better, longer string (higher number) is taken as multiplicand.
#The shorter string(smaller number) is assigned as multiplier to define the number of iterations
#Smaller number means lesser iterations
if (n2 > n1):
    multiplier_string, multiplicand_string = multiplicand_string, multiplier_string
    n2, n1 = n1, n2
    
#This quantum register will store the values of repeated summation of multiplicand until multiplier is zero
accumulator = QuantumRegister(n)
#This quantum register will decrease the value of multiplier by 1 after every iteration
decrementer = QuantumRegister(1)

#Quantum registers to store multiplicand and multiplier
multiplicand = QuantumRegister(n1)
multiplier = QuantumRegister(n2)

c_reg = ClassicalRegister(n)

qc = QuantumCircuit(accumulator, multiplier, multiplicand, decrementer, c_reg, name = "circuit")

#Setting the decrementer to state |1>
qc.x(decrementer)

#Storing numbers in the multiplicand and multiplier registers according to user input
for i in range(n1):
    if (multiplicand_string[i] == '1'):
        #The index here is written so as take care of the different ordering in classical
        #and quantum programming (particularly Qiskit)
        qc.x(multiplicand[n1-i-1])

for i in range(n2):
    if (multiplier_string[i] == '1'):
        qc.x(multiplier[n2-i-1])

#This is initially set to 1. Once the multiplier string goes to zero, this will switch to zero as well and stop the loop
#The need for this arises because of absence of a controlled gate that tells the program to stop doing iterations
multiplier_stopper = '1'

#This loop adds the multiplicand multiple times and decreases the multiplier with each iteration till the multiplier is zero
#Result of the experiment are stored in the "counts" variable duting the processing
while(int(multiplier_stopper) != 0):
    #This function call is to add multiplicand and store it in accumulator
    summation(accumulator, multiplicand, qc, 1)
    
    #This function call is to decrease the value of multiplier by 1
    summation(multiplier, decrementer, qc, -1)
    
    for i in range(len(multiplier)):
        qc.measure(multiplier[i], c_reg[i])
    job = execute(qc, backend = Aer.get_backend('qasm_simulator'), shots = 2)
    counts = job.result().get_counts(qc)
    multiplier_stopper = list(counts.keys())[0]

qc.measure(accumulator, c_reg)

job = execute(qc, backend = Aer.get_backend('qasm_simulator'), shots = 2)
counts = job.result().get_counts(qc)

print("")
#The counts variable is in dictionary form which doesn't suit purpose of this program so we use the below form
print("The product is:", int(next(iter(counts)),2))
