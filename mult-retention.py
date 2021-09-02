from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from numpy.random import randint
import numpy as np
import matplotlib.pyplot as plt
# print("Imports Successful")

def encode_message(n, bits, bases):
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

def measure_message(n, message, bases):
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

def remove_garbage(n, a_bases, b_bases, bits):
    good_bits = []
    for q in range(n):
        if a_bases[q] == b_bases[q]:
            # If both used the same basis, add
            # this to the list of 'good' bits
            good_bits.append(bits[q])
    return good_bits

def bb84(n):

    alice_bits = randint(2, size=n)

    alice_bases = randint(2, size=n)
    message = encode_message(n, alice_bits, alice_bases)

    bob_bases = randint(2, size=n)

    bob_results = measure_message(n, message, bob_bases)

    # Step 4
    alice_key = remove_garbage(n, alice_bases, bob_bases, alice_bits)
    bob_key = remove_garbage(n, alice_bases, bob_bases, bob_results)

    if bob_key == alice_key:
        shared_key = bob_key
        return len(shared_key)
    else:
        print("Error")

def avg(dataset):
    sum = 0
    count = 0
    for i in range(0, len(dataset)):
        sum += dataset[i]
        count += 1
    return sum/count

def next_narr(n_vals, index):
    output = []
    for i in range(0, TRIALS):
        output.append(n_vals[index])
    return output

n_vals = [15, 20, 25, 30, 35, 40, 45, 50]
data = {n_vals[0]:[],n_vals[1]:[],n_vals[2]:[],n_vals[3]:[],n_vals[4]:[],n_vals[5]:[],n_vals[6]:[],n_vals[7]:[]}
TRIALS = 10

for i in range(0, len(n_vals)):
    for j in range(0, TRIALS):
        datapt = bb84(n_vals[i])
        data[n_vals[i]].append(datapt)

# print(data)

averages = {n_vals[0]:None,n_vals[1]:None,n_vals[2]:None,n_vals[3]:None,n_vals[4]:None,n_vals[5]:None,n_vals[6]:None,n_vals[7]:None}
avg_arr = []
for i in range(0, len(n_vals)):
    datapt = avg(data[n_vals[i]])
    averages[n_vals[i]] = datapt
    avg_arr.append(datapt)

##VISUALIZATION
#add figure from canvas coordinates (0.1, 0,1) to (0.9,0.9)
fig = plt.figure()
ax = fig.add_axes([0.1,0.1,0.8,0.8]) #(x, y, len, wid)

diag1 = np.array(range(60))
diag2 = []
diag3 = []
for val in diag1:
    diag2.append(val/2)
for val in diag1:
    diag3.append(val/1.667)


multiple = [8, 12, 15, 18, 22, 25, 28, 31]

perfect, = plt.plot(diag1, diag1, '--')
half, = plt.plot(diag1, diag2, 'g--')
expected, = plt.plot(diag1, diag3, '-', color='orange')

avgs, = plt.plot(n_vals, avg_arr, 'p', color='gray',
         markersize=15,
         markerfacecolor='white',
         markeredgecolor='gray',
         markeredgewidth=2)

plt.xlim(0, 55)
plt.ylim(0, 55)
# plt.gca().set_aspect('equal', adjustable='box')

ineff = ax.fill_between(diag1, diag1, diag2,facecolor='gray',alpha=0.3)

# ax.legend([run, avgs, perfect, half, ineff],['Trial Result', 'Averages', 'Perfect Retention', '50% Retention', 'Inefficiency'], loc = 'upper left') # legend placed at lower right

ax.legend(labels = ('Perfect Retention', '50% Retention', 'Possible Enhanced Retention', 'Current BB84 Averages', 'Inefficiency'), loc = 'upper left') # legend placed at lower right
ax.set_title("Expected QKD Efficiency as Entanglement Pair Concentration Increases")
ax.set_xlabel('N (Total Number of Qubits)')
ax.set_ylabel('Retention (Number of Qubits)')
plt.show()
