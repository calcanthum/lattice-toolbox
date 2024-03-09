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
        
        if not all(isinstance(row, (list, tuple)) and all(isinstance(x, int) for x in row) for row in basis_matrix):
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
        Generate a 'bad' basis matrix for an identity lattice of a given dimension.
        This method selects two random points on the lattice to create new basis vectors,
        ensuring the resulting basis is related to the original lattice structure.
        """
        identity_matrix = Matrix.eye(dimension)
        
        if not isinstance(dimension, int) or dimension <= 0:
            raise ValueError("Dimension must be a positive integer.")

        if modulus is not None:
            if not isinstance(modulus, int) or modulus <= 0:
                raise ValueError("Modulus must be a positive integer.")

        bad_matrix = Matrix.zeros(dimension)

        for i in range(dimension):
            point = [random.randint(randomness_range[0], randomness_range[1]) for _ in range(dimension)]
            lattice_point = identity_matrix * Matrix(point)

            if modulus:
                lattice_point = lattice_point.applyfunc(lambda x: x % modulus)

            for j in range(dimension):
                bad_matrix[j, i] = lattice_point[j]
        
        return bad_matrix
    
    @staticmethod
    def generate_good_basis(dimension, modulus=None):
        """
        Generate a 'good' basis matrix, which is simply the identity matrix for the lattice of a given dimension.
        """
        return Matrix.eye(dimension)

class Parallelepiped:
    def __init__(self, lattice, vectors):
        """
        Initialize the Parallelepiped with a reference lattice and defining vectors.
        """
        self.lattice = lattice
        self.vectors = Matrix(vectors).transpose()
        
        if self.vectors.rows != self.lattice.basis_matrix.rows:
            raise ValueError("Vector dimensions must match the lattice basis dimensions.")
        if not all(isinstance(row, (list, tuple)) and all(isinstance(x, int) for x in row) for row in vectors):
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
