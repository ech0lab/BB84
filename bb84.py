#!/usr/bin/python3
"""
BB84 avec qiskit
"""
import argparse
import numpy as np
from numpy.random import randint
from qiskit import QuantumCircuit, Aer, assemble


parser = argparse.ArgumentParser()
parser.add_argument("-k", "--key",
        type = int,
        default=128 ,
        help = "Taille de la clé, defaut : 128")

parser.add_argument("-i", "--intercept",
        action='store_true',
        help = "Interception du message par Eve")

parser.add_argument("-c", "--check",
        type = int,
        default=20,
        help = "Nombre de qubits à vérifier, defaut : 20")

args = parser.parse_args()

def encode_message(bits, bases):
    """
    Fonction pour encoder la suite de qubits d'Alice
    """
    msg = []
    for i in range(N):
        qc_em = QuantumCircuit(1,1)
        if bases[i] == 0:
            if bits[i] == 0:
                pass
            else:
                # Coder le qubit avec la base x
                qc_em.x(0)
        else:
            if bits[i] == 0:
                # Coder le qubit en base +
                qc_em.h(0)
            else:
                # Coder le bit en base x puis en base +
                qc_em.x(0)
                qc_em.h(0)
        # Envoyer les qubits
        qc_em.barrier()
        msg.append(qc_em)
    return msg

def measure_message(msg, bases):
    """
    Fonction pour la mesure des qubits par Bob
    """
    Aer.get_backend('aer_simulator')
    measurements = []
    for i in range(N):
        if bases[i] == 0:
            # Mesure en base +
            msg[i].measure(0,0)
        if bases[i] == 1:
            # Mesure en base x
            msg[i].h(0)
            msg[i].measure(0,0)
        # Simulation pour avoir la valeurs des qubits mesurés
        aer_sim = Aer.get_backend('aer_simulator')
        qobj = assemble(msg[i], shots=1, memory=True)
        result = aer_sim.run(qobj).result()
        measured_bit = int(result.get_memory()[0])
        measurements.append(measured_bit)
    return measurements

def remove_garbage(a_bases, b_bases, bits):
    """
    Fonction pour supprimer les qubits mesurer avec une base différente
    """
    good_bits = []
    for i in range(N):
        if a_bases[i] == b_bases[i]:
            # Si les bases d'Alice et Bob pour un qubits sont les même, garder le qubits
            good_bits.append(bits[i])
    return good_bits

def sample_bits(bits, selection):
    """
    Comparaison d'un nombre aléatoire de qubits pour voir
    s'ils n'ont pas été modifier par une mesure
    """
    sample = []
    for i in selection:
        # Si les qubits envoyer et mesurer dans la même base ont la même valeurs
        i = np.mod(i, len(bits))
        sample.append(bits.pop(i))
    return sample

# Genération aléatoire de N bits par Alice
np.random.seed(seed=0)
N = int(args.key)
alice_bits = randint(2, size=N)

# Genération aléatoire de bases pour chaque bits
alice_bases = randint(2, size=N)

# Encodage des bits d'Alice avec les bases
message = encode_message(alice_bits, alice_bases)

# Genération aléatoire de N bases pour Eve
if args.intercept:
    eve_bases = randint(2, size=N)
    intercepted_message = measure_message(message, eve_bases)

# Genération aléatoire de N bases pour Bob
bob_bases = randint(2, size=N)

# Mesure des qubits d'Alice par Bob avec ses bases
bob_results = measure_message(message, bob_bases)

# Retirer les qubits qui n'ont pas été envoyer en mesurer avec la même base pour les bits d'Alice
alice_key = remove_garbage(alice_bases, bob_bases, alice_bits)

# Retirer les qubits qui n'ont pas été envoyer en mesurer avec la même base pour les bits de Bob
bob_key = remove_garbage(alice_bases, bob_bases, bob_results)

# Prendre n qubits aléatoire et comparer les résulats pour voir s'ils sont cohérents
SAMPLE_SIZE = int(args.check)
bit_selection = randint(N, size=SAMPLE_SIZE)

# Comparaison des bits d'Alice et Bob
bob_sample = sample_bits(bob_key, bit_selection)
alice_sample = sample_bits(alice_key, bit_selection)

# Vérification qu'il n'y à pas eu d'interception
print(f"\nClé de {len(alice_key)} bits : \n")
print("Alice Key : ", end="")
for a in alice_key:
    print(a, end="")
print()
print("Bob Key   : ", end="")
for b in bob_key:
    print(b, end="")
print()
if bob_sample == alice_sample:
    print("\nPas d'interception détectée\n")
else:
    print("\nInterception détectée\n")
