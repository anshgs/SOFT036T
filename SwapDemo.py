from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from numpy.random import randint
import numpy as np
import math
import random
print("Imports Successful")

def encode_message(bits, bases):
    message = []
    for i in range(n):
        qc = QuantumCircuit(1,1)
        if bases[i] == 0: # Prepare qubit in Z-basis
            if bits[i] == 0:
                pass
            else:
                qc.x(0)
        else: # Prepare qubit in X-basis
            if bits[i] == 0:
                qc.h(0)
            else:
                qc.x(0)
                qc.h(0)
        qc.barrier()
        message.append(qc)
    return message

def encode_signed_message(bits, bases, signature):
    message = []
    for i in range(n):
        fakeSign = randint(3, size=m)
        forgery = create_sign(fakeSign)
        if forging:
            signature = forgery
        qc = QuantumCircuit(1,1)
        if bases[i] == 0: # Prepare qubit in Z-basis
            if bits[i] == 0:
                pass
            else:
                qc.x(0)
        else: # Prepare qubit in X-basis
            if bits[i] == 0:
                qc.h(0)
            else:
                qc.x(0)
                qc.h(0)
        message.append(qc)
        qc.barrier()
        for j in range(m):
            message.append(signature[j])
    return message

def measure_message(message, bases):
    backend = Aer.get_backend('qasm_simulator')
    measurements = []
    for q in range(n):
        if bases[q] == 0: # measuring in Z-basis
            message[q].measure(0,0)
        if bases[q] == 1: # measuring in X-basis
            message[q].h(0)
            message[q].measure(0,0)
        result = execute(message[q], backend, shots=1, memory=True).result()
        measured_bit = int(result.get_memory()[0])
        measurements.append(measured_bit)
    return measurements

def measure_signed_message(message, bases, copySign):
    backend = Aer.get_backend('qasm_simulator')
    measurements = []
    signTest = []
    errorCountArr = []
    for q in range(n):
        recSig = []
        if bases[q] == 0: # measuring in Z-basis
            message[q*(m+1)].measure(0,0)
        if bases[q] == 1: # measuring in X-basis
            message[q*(m+1)].h(0)
            message[q*(m+1)].measure(0,0)
        for i in range(m):
            recSig.append(message[q*(m+1)+1+i])
        signTest.append(checkSign(recSig, copySign))
        result = execute(message[q*(m+1)], backend, shots=1, memory=True).result()
        measured_bit = int(result.get_memory()[0])
        measurements.append(measured_bit)
    for e in range(n):
        errorCount = 0;
        for d in range(m):
            if signTest[e][d] == 1:
                errorCount = errorCount+1
        errorCountArr.append(errorCount)
    return measurements, errorCountArr

def remove_garbage(a_bases, b_bases, bits):
    good_bits = []
    for q in range(n):
        if a_bases[q] == b_bases[q]:
            # If both used the same basis, add
            # this to the list of 'good' bits
            good_bits.append(bits[q])
    return good_bits

def create_sign(value):
    signature = []
    for i in range(m):
        qc = QuantumCircuit(1,1)
        qc.rx(2*value[i]*math.pi/(b-1), 0)
        qc.barrier()
        signature.append(qc)
    return signature

def create_sign(value, mapping):
    signature = []
    for i in range(m):
        qc = QuantumCircuit(1,1)
        qc.rx(mapping[value[i]], 0)
        qc.barrier()
        signature.append(qc)
    return signature

def checkSign(actual, test):
	backend = Aer.get_backend('qasm_simulator')
	output = []
	for i in range(m):
		qc = QuantumCircuit(3, 1)
		qc.h(0);
		qc = qc.compose(actual[i], [1])
		qc = qc.compose(test[i], [2])
		qc.cx(2,1)
		qc.ccx(0,1,2)
		qc.cx(2,1)
		qc.h(0)
		qc.measure(0,0)
		result = execute(qc, backend, shots=1, memory=True).result()
		measured_bit = int(result.get_memory()[0])
		output.append(measured_bit)
	return output

np.random.seed(seed=0)
print("Enter specifications for protocol") #A+B ALREADY KNOW THIS (protocol)
b = int(input("Base to encode in: "))
n = int(input("Length of message: "))
m = int(input("Length of signature: "))
forging = (input("Forging?(Yes(1)/No(0)): ") == "1")

## Step 1
# Alice generates bits and signature
alice_bits = randint(2, size=n)
alice_sign = randint(b, size=m)
alice_angles_txt = []
alice_angles_val = []
fake_angles_txt = []
fake_angles_val = []



tempfakeSign = []
if(forging):
    ownForge = (input("Would you like to create the forged signature yourself?(Yes(1)/No(0)): ") == "1")
    if(ownForge):
        print("Enter " + str(m) + " values from 0 to " + str(b-1))
        for i in range(b):
            tempfakeSign.append(int(input("Enter value " + str(i+1)+"/"+str(m) + ": ")))
        print("Enter " + str(m) + " angles from 0 to 2" + '\u03C0' + ":")
        for i in range(b):
            fake_angles_val.append(float(input("Enter angle " + str(i+1)+"/"+str(m) + ": ")))
        fake_angles_txt = fake_angles_val
        fakeSign = tempfakeSign
    else:
        fakeSign = randint(b, size=m)
        for i in range(b):
            fake_angles_val.append(2*random.random()*math.pi)
            fake_angles_txt.append(str(round(2*random.random(), 2))+"pi")
    print("Forged Signature(Before Encoding Into Qubits)")
    print(fakeSign)
    print("Forged Private Key Angles(representing 0 to n-1)")
    print(fake_angles_txt)

print("Alice's Signature(Before Encoding Into Qubits)")
print(alice_sign)
print("Alice's Private Key Angles(representing 0 to n-1)")
for i in range(b):
    #alice_angles_txt.append(str(2*i)+"pi/"+str(b)) optional fixed angles uniformly distributed
    #alice_angles_val.append(2*i*math.pi/b)
    alice_angles_val.append(2*random.random()*math.pi)
    alice_angles_txt.append(str(round(2*random.random(), 2))+"pi")
print(alice_angles_txt)

userSign = alice_sign
user_angles_val = alice_angles_val

if(forging):
    userSign = fakeSign
    user_angles_val = fake_angles_val    

print("Swap test with signature")
output = (checkSign(create_sign(alice_sign, alice_angles_val), create_sign(userSign, user_angles_val)))
print(output)
errors = False
for i in output:
    if(i==1): 
        errors=True
if(errors): print("Errors detected - forgery is highly likely")
else: print("No errors detected - correct sender highly likely")