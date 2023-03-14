# Implémentation de BB84 avec qiskit

* Requirements :
```
qiskit 0.42.0
```

* Arguments : 

```
usage: bb84.py [-h] [-k KEY] [-i] [-c CHECK]

optional arguments:
  -k KEY, --key KEY     Taille de la clé, defaut : 128
  -i, --intercept       Interception du message par Eve
  -c CHECK, --check CHECK
                        Nombre de qubits à vérifier, defaut : 20
```

* Bibliographie :

https://qiskit.org/textbook/ch-algorithms/quantum-key-distribution.html
