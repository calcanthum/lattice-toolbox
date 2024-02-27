from sympy import Matrix, solve_linear_system, symbols
from sympy.solvers.solveset import linsolve
import itertools
import random

class Lattice:
    def __init__(self, basis_matrix, modulus=None):
        """
        Initialize the Lattice object with a basis matrix for any dimension and a modulus value for arithmetic operations.
        """
        self.basis_matrix = Matrix(basis_matrix)
        self.modulus = modulus
        
        if self.basis_matrix.rows != self.basis_matrix.cols:
            raise ValueError("Basis matrix must be square (n x n).")
        
        if self.modulus is not None:
            if not isinstance(self.modulus, int) or self.modulus <= 0:
                raise ValueError("Modulus must be a positive integer.")
        
        if not all(isinstance(row, (list, tuple)) and all(isinstance(x, (int, float)) for x in row) for row in basis_matrix):
            raise ValueError("Basis matrix must contain only numbers in lists or tuples.")
        
    def generate_points(self, *ranges):
        """
        Generate lattice points within the specified ranges for any dimensions.
        """
        if len(ranges) != self.basis_matrix.rows:
            raise ValueError(f"Number of ranges ({len(ranges)}) must match the basis matrix dimension ({self.basis_matrix.rows}).")

        grids = [range(r[0], r[1] + 1) for r in ranges]
        all_points = list(itertools.product(*grids))

        if not all(isinstance(r, tuple) and len(r) == 2 and all(isinstance(x, int) for x in r) and r[0] <= r[1] for r in ranges):
            raise ValueError("Ranges must be tuples of two integers where the first is ≤ the second.")

        if self.modulus:
            points = [(self.basis_matrix * Matrix(point)).applyfunc(lambda x: x % self.modulus) for point in all_points]
        else:
            points = [self.basis_matrix * Matrix(point) for point in all_points]
        return [tuple(point) for point in points]
    
    def get_determinant(self):
        """
        Calculate the determinant of the basis matrix.
        """
        if self.modulus:
            return self.basis_matrix.det() % self.modulus
        else:
            return self.basis_matrix.det()


class LatticeMatrix:
    @staticmethod
    def generate_bad_basis(dimension, randomness_range=(1, 10), modulus=None):
        """
        Generate a 'bad' basis matrix for an identity lattice of a given dimension
        while ensuring the transformations are unimodular (determinant is ±1).
        """
        identity_matrix = Matrix.eye(dimension)
        bad_matrix = identity_matrix.copy()

        if not isinstance(dimension, int) or dimension <= 0:
            raise ValueError("Dimension must be a positive integer.")
        
        if not (isinstance(randomness_range, tuple) and len(randomness_range) == 2 and all(isinstance(x, int) for x in randomness_range) and randomness_range[0] <= randomness_range[1]):
            raise ValueError("Randomness range must be a tuple of two integers where the first is ≤ the second.")
  
        for _ in range(dimension * 2):
            i, j = random.sample(range(dimension), 2)
            if i != j:
                shear_factor = random.randint(randomness_range[0], randomness_range[1])
                for k in range(dimension):
                    new_value = bad_matrix[i, k] + shear_factor * bad_matrix[j, k]
                    bad_matrix[i, k] = new_value % modulus if modulus is not None else new_value

        # Ensure the determinant is ±1
        while bad_matrix.det() not in [1, -1]:
            if modulus is not None:
                bad_matrix = Matrix(dimension, dimension, lambda i, j: random.randint(-modulus, modulus - 1) % modulus)
            else:
                bad_matrix = Matrix(dimension, dimension, lambda i, j: random.randint(-10, 9))

        return bad_matrix
    
    @staticmethod
    def generate_good_basis(dimension, modulus=None):
        """
        Generate a good basis matrix for a lattice of a given dimension.
        """
        if not isinstance(dimension, int) or dimension <= 0:
            raise ValueError("Dimension must be a positive integer.")
        
        good_basis = Matrix.eye(dimension)    
        return good_basis


class Parallelepiped:
    def __init__(self, lattice, vectors):
        """
        Initialize the Parallelepiped with a reference lattice and defining vectors.
        """
        self.lattice = lattice
        self.vectors = Matrix(vectors).transpose()
        
        if self.vectors.rows != self.lattice.basis_matrix.rows:
            raise ValueError("Vector dimensions must match the lattice basis dimensions.")
        if not all(isinstance(row, (list, tuple)) and all(isinstance(x, (int, float)) for x in row) for row in vectors):
            raise ValueError("Vectors must contain only numbers in lists or tuples.")
   
    def volume(self):
        """
        Calculate the volume of the parallelepiped.
        """
        return abs(self.vectors.det())
    
    def contains_point(self, point):
        """
        Determine if a given point is inside the parallelepiped.
        """
        n = self.vectors.rows
        symbols_list = symbols(f'a0:{n}')
        equations = self.vectors * Matrix(symbols_list) - Matrix(point)
        
        solution = linsolve(equations, symbols_list)
        
        if solution:
            solution = next(iter(solution))
            return all(0 <= sol <= 1 for sol in solution)
        else:
            return False


class LatticeCrypto:
    def __init__(self, dimension, modulus=None):
        self.dimension = dimension
        self.modulus = modulus

        if not isinstance(dimension, int) or dimension <= 0:
            raise ValueError("Dimension must be a positive integer.")

    def generate_keys(self):
        private_basis = LatticeMatrix.generate_good_basis(self.dimension, modulus=None)
        noise = self.generate_noise()
        public_basis = private_basis + noise
        return (public_basis, private_basis)

    def generate_noise(self):
        random_range = 5 * self.dimension 
        noise_matrix = Matrix(self.dimension, self.dimension, lambda i, j: random.randint(-random_range, random_range))
        if self.modulus:
            noise_matrix = noise_matrix.applyfunc(lambda x: x % self.modulus)
        return noise_matrix