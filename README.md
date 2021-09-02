# SOFT036T
ISEF 2021 SOFT036T: Improving Upon Quantum Cryptography Protocols Using Entanglement and Quantum Signatures

Code repository for ISEF 2021 project SOFT036T by Ansh Sharma and Rohan Kulkarni

BB84.py contains an implementation of the base BB84 algorithm. 

SwapDemo.py demonstrates the quantum signature scheme, allowing the user to decide the length and base of the signature/message as well as whether to forge the signature or not. User also has the option to create their own forgery or instead use a fully random forged signature for demonstrative purposes. 

EntanglementScheme.py demonstrates the entanglement scheme with 1 entangled pair chosen by the user out of 10 qubits being sent across, but can be adjusted for larger messages. Currently only supports a single entanglement pair.
