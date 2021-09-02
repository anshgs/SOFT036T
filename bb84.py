from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from numpy.random import randint
import numpy as np
# print("Imports Successful")

def encode_message(bits, bases):
    message = []
    for i in range(n):
        qc = QuantumCircuit(1,1)
        if bases[i] == 0: # Prepare qubit in Z-basis
            if bits[i] == 0:
                pass # |0>
            else:
                qc.x(0) # |1>
        else: # Prepare qubit in X-basis
            if bits[i] == 0:
                qc.h(0) # |+>
            else:
                qc.x(0)
                qc.h(0) # |->
        qc.barrier()
        message.append(qc)
    return message

def measure_message(message, bases):
    backend = Aer.get_backend('qasm_simulator')
    measurements = [None]*n #create measurement list

    for q in range(n):
        if bases[q] == 0: # measuring in Z-basis
            message[q].measure(0,0)
        if bases[q] == 1: # measuring in X-basis
            message[q].h(0)
            message[q].measure(0,0)
        result = execute(message[q], backend, shots=1, memory=True).result()
        counts = result.get_counts(message[q])
        measured_bit = int(next(iter(counts)))
        measurements[q] = measured_bit

    return measurements

def remove_garbage(a_bases, b_bases, bits):
    good_bits = []
    for q in range(n):
        if a_bases[q] == b_bases[q]:
            # If both used the same basis, add
            # this to the list of 'good' bits
            good_bits.append(bits[q])
    return good_bits


n = 20

## Step 1
# Alice generates bits
alice_bits = randint(2, size=n)

## Step 2
# Create an array to tell us which qubits
# are encoded in which bases
alice_bases = randint(2, size=n)
message = encode_message(alice_bits, alice_bases)

## Step 3
# Decide which basis to measure in:
bob_bases = randint(2, size=n)

bob_results = measure_message(message, bob_bases)

print("Bob unfiltered:")
print(bob_results)

print("Length (should be n): " + str(len(bob_results)))

# Step 4
alice_key = remove_garbage(alice_bases, bob_bases, alice_bits)
bob_key = remove_garbage(alice_bases, bob_bases, bob_results)

print("Bob filtered:")
print(bob_key)
print("Bob Key Length: " + str(len(bob_key)))
print("Alice Key Length (should be same ^): " + str(len(alice_key)))

if bob_key == alice_key:
    print("Shared Key:")
    print(alice_key)
else:
    print("Error")
