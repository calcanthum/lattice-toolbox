# Import the LatticeCrypto class from the lattice module
from lattice import LatticeCrypto

def run_hello_world_crypto():
    # Set up the dimension and modulus for the LatticeCrypto system
    dimension = 2  # Example: 4-dimensional lattice
    modulus = 101  # Example modulus; choose based on your cryptographic needs

    # Initialize the LatticeCrypto system with the specified dimension and modulus
    crypto_system = LatticeCrypto(dimension, modulus=modulus)

    # Generate the public and private keys
    public_basis, private_basis = crypto_system.generate_keys()

    # Print out the generated keys to demonstrate the functionality
    print("Generated Public Basis:")
    print(public_basis)
    print("\nGenerated Private Basis:")
    print(private_basis)

if __name__ == "__main__":
    run_hello_world_crypto()
