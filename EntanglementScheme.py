from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from numpy.random import randint
import numpy as np
# print("Imports Successful")

print("BITS TO ENTANGLE") #A+B ALREADY KNOW THIS (protocol)
b1 = int(input("Bit 1: "))
b2 = int(input("Bit 2: "))
entangled = (b1, b2)

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

def simple_entangle(e1, e2, arr):

    #method simple_entangle entangles qubits with H-CX bell-pair producer
    #measurements of entangled qubits are assumed to be in the simple Z axis
    #added functionality (i.e. inverse entanglement, entanglement in X basis) will added in later

    eqc = QuantumCircuit(2,2)

    eqc.h(0)
    eqc.cx(0,1)
    eqc.barrier()

    del arr[e1]
    arr.insert(e1, eqc)
    #the actual message cannot be sent with the "placeholder" message
    #then, eve would know that bit is entangled with another
    #so, position of secondary entangled bit e2 is held constant (indistinguishable)

    return arr

def measure_message(message, bases):
    backend = Aer.get_backend('qasm_simulator')
    measurements = [None]*n #create measurement list
    entangle_done = False

    for q in range(n):
        if (entangle_done == False) or (q != entangled[1]):

            if len(message[q].qubits) == 2: #if the state is entangled

                #Bob identifies which entangled bit he has encountered:
                if q == entangled[0]:
                    print("Primary Entangled Bit Found")
                    other = entangled[1]
                else:
                    other = entangled[0]

                if bases[q] == 0: # TEMP: measuring in Z-basis
                    message[q].measure(0,0)
                    message[q].measure(1,1)
                result = execute(message[q], backend, shots=1, memory=True).result()
                counts = result.get_counts(message[q])
                primary_bit = next(iter(counts))[0] #[0] ensures that only measurement of ONE qubit is added to the result
                primary_bit = primary_bit + "*" #TEMP
                measurements[q] = primary_bit

                #you've added in the primary entangled bit, now replace or add in the second one
                secondary_bit = next(iter(counts))[1] #[1] ensures that only measurement of SECOND qubit is added to the result
                secondary_bit = secondary_bit + "*" #TEMP
                measurements[other] = secondary_bit
                entangle_done = True

            else: #normal bits
                if bases[q] == 0: # measuring in Z-basis
                    message[q].measure(0,0)
                if bases[q] == 1: # measuring in X-basis
                    message[q].h(0)
                    message[q].measure(0,0)
                result = execute(message[q], backend, shots=1, memory=True).result()
                counts = result.get_counts(message[q])
                measured_bit = next(iter(counts))
                measurements[q] = measured_bit
        else:
            entangle_done = False #resets as if entanglement didn't happen

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

print("BEFORE ENTANGLEMENT:")

print("Base: " + str(alice_bases[b1]) + "; Bit: " + str(alice_bits[b1]))
print(message[b1]);

print()

print("Base: " + str(alice_bases[b2]) + "; Bit: " + str(alice_bits[b2]))
print(message[b2]);

print()
print("AFTER ENTANGLEMENT:")
res = simple_entangle(b1, b2, message)
print(res[b1])
print(res[b2])

## Step 3
# Decide which basis to measure in:
bob_bases = randint(2, size=n)

#TEMP: Adjust for Bob polarizer to measure in simple Z basis
bob_bases[b1] = 0
bob_bases[b2] = 0

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
print(alice_key)
if bob_key == alice_key:
    print("Shared Key:")
    print(alice_key)
else:
    print("Error")
