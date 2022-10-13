# MULTIPLYING TWO NUMBERS USING QISKIT

Among given four tasks I chose the first one and created a function 'multiplication' that takes two numbers as its input and returns the value of their product.
As instructed, this has been done using Quantum gates. The backbone of this algorithm is Quantum Fourier Transform which does repeated additions to calculate the desired result. This short writeup is to provide necessary prerequisites and give answers to some bonus questions mentioned in the task. Although necesary comments have been added in the python file itself to explain what's happening at each step, **this writeup will help better understand the reasoning behind what's being done in the code**.

### If you would like to jump ahead and read the code straight away, here's the python file: [Multiplication using Quantum Algorithm](https://github.com/RajatLakhera/Q.C.-Projects/blob/6ab5bd48fafe3e893a69e5c723b2edf06cb19d04/Quantum%20Multiplication.py)


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

## Results
I ran the algorithm by giving different inputs to the function. In addition to printing the result, other things like: time of execution, circuit depth, number of
qubits and number of gates were also calculated using in-built Qiskit functions. Here are some of the results:

![Screenshot (1609)-tile](https://user-images.githubusercontent.com/84754754/195525217-a3f1e141-275c-49ab-9ada-37c2a4904afe.jpg)

As can be seen from these results, the execution time increases exponentially with increase in number of qubits. This directly causes greater demand for memory/
processing power. So large circuit depth and width are an issue for this function. 

I tried to input higher numbers in the function, at which point the program started to use half of the system's RAM. Clearly product of double digit numbers (around 40-45) can't be simulated using a normal specs pc. The highest number of qubits that I was able to simulate using this function is 34.  Researchers have simulated upto 61 qubits using Supercomputers. So that seems to be the present limit for simulating qubits. 
