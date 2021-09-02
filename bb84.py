from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from numpy.random import randint
import numpy as np
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
        if value[i] == 0: 
            pass
        elif value[i] == 1: 
            qc.h(0)
        else:
            qc.x(0)
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
n = 20
m = 10
forging = False
if forging:
    print("Using forged signature")
else:
    print("Using actual signature")
## Step 1
# Alice generates bits and signature
alice_bits = randint(2, size=n)
alice_sign = randint(3, size=m)
## Step 2
# Create an array to tell us which qubits
# are encoded in which bases
alice_bases = randint(2, size=n)
#message = encode_message(alice_bits, alice_bases)
originalSign = create_sign(alice_sign)
signedMessage = encode_signed_message(alice_bits, alice_bases, originalSign)

## Step 3
# Decide which basis to measure in:
bob_bases = randint(2, size=n)
#bob_results = measure_message(message, bob_bases)
recievedSign = create_sign(alice_sign)
#print("Recieved:")
#print(alice_sign)
bob_signed_results, bob_verification = measure_signed_message(signedMessage, bob_bases, recievedSign)


print("Bob unfiltered:")
print(bob_signed_results)
print("Length (should be n): " + str(len(bob_signed_results)))

print("Error Counts in each signature:")
print(bob_verification)

#fakeSign = randint(3, size=m)
#print("Fake:")
#print(fakeSign)
#forgery = create_sign(fakeSign)

#print("Checking Correct Signature Validity")
#signChecker = checkSign(originalSign, recievedSign);
#print(signChecker)

#print("Checking False Signature Validity")
#signChecker = checkSign(forgery, recievedSign);
#print(signChecker)

#print(bob_results)
#print(bob_signed_results)

## Step 4
alice_key = remove_garbage(alice_bases, bob_bases, alice_bits)
bob_key = remove_garbage(alice_bases, bob_bases, bob_signed_results)

print("Bob filtered:")
print(bob_key)
print("Bob Key Length: " + str(len(bob_key)))
print("Alice Key Length (should be same ^): " + str(len(alice_key)))

if bob_key == alice_key:
    print("Shared Key:")
    print(alice_key)
else:
    print("Error")
