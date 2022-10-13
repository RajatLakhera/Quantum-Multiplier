# MULTIPLYING TWO NUMBERS USING QISKIT

Among given four tasks I chose the first one and crated a function 'multiplication' that takes two numbers as its input and returns the value of their product.
As instructed, this has been done using Quantum gates. The backbone of this algorithm is Quantum Fourier Transform which does repeated additions alongwith bit shift
to calculate the desired result. This short writeup is to provide necessary prerequisites and give answers to some bonus questions mentioned in the task. Although 
necesary comments have been added in the python file itself to explain what's happening at each step, **this writeup will help better understand the reasoning behind
what's being done in the code**.

### If you would like to jump ahead and read the code straight away, here's the python file: [Multiplication using Quantum Algorithm](https://github.com/RajatLakhera/QOSF-Screening-Task/blob/23cd3fdaf9c954ce8788da63854aa955f0140369/Multiplication%20using%20Quantum%20Algorithm.py)


## Why use Fourier Transform?
Fourier Transform is frequently used in Quantum Mechanics to transition from position space to momentum space (and vice-versa). Graphically F.T. could be thought of as
using periodic functions like sine and cosine to create any other funciton. In Quantum Computing F.T. translates to performing phase rotations.

Usually coding is done in computational basis: { |0> , |1> }. Quantum Fourier Transform (Q.F.T.) converts this to the fourier basis: { |+> , |-> }. So thinking in terms
of single qubit representation on Bloch Sphere, Q.F.T. takes the vector from pointing to poles (computational basis) to pointing towards the equator (fourier basis)
where phase rotations can be applied. 

Thus, Q.F.T. essentially introduces a phase through an exponential term in front of the computational basis state |1>. This is useful because now if one needs to add two
(or more) qubits, it can be done by doing some phase rotations. Owing to the property of exponentials, repeated phase rotations introduce more and more exponential terms
which ends up adding the powers of exponential terms. Once the addition is complete, Inverse Fourier Transform can be applied to take the qubits back to computational basis.


## Essentials for implementation
Q.F.T. in this algorithm uses two Quantum gates for implementation:
- Hadamard Gate, and
- Controlled-Phase Gate
   
 Using these two gates alone Q.F.T. can be performed. One thing that needs to be taken care of here is the different ordering of qubits in Qiskit. This issue is 
 resolved either by using swap gates or by making some adjustments in indices of loops and conditional statements in the code. I've used the latter one. 


## How does the code work?
The two numbers received by 'multiplication' function are converted from decimal to binary form. The greater of the two numbers (here multiplicannd) is operated 
by the 'QFT' function which converts it into Fourier Basis. Then using another function, multiplicand is added repetitively using another register: 'adder'. The
number of iterations here is decided by the multiplier register. With each addition of multiplicand, the multiplier is decreased by 1 and addition is stopped when
multiplicand becomes zero. 

## BONUS TASKS
