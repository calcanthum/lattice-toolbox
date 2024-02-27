import unittest
from lattice import Lattice, LatticeMatrix, Parallelepiped  

class TestLattice2D(unittest.TestCase):

    def setUp(self):
        self.basis_matrix = [[1, 0], [0, 1]]
        self.lattice = Lattice(self.basis_matrix)

    def test_init(self):
        self.assertIsInstance(self.lattice, Lattice)

    def test_lattice_init_non_square_matrix_raises_error(self):
        with self.assertRaises(ValueError):
            Lattice([[1, 0]])  

    def test_generate_points(self):
        ranges = ((-1, 1), (-1, 1))
        expected_points = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        actual_points = self.lattice.generate_points(*ranges)
        self.assertEqual(set(expected_points), set(actual_points), "Generated points do not match expected.")

    def test_generate_points_with_negative_ranges(self):
        ranges = ((-2, -1), (-2, -1))
        expected_points = [(-2, -2), (-2, -1), (-1, -2), (-1, -1)]
        actual_points = self.lattice.generate_points(*ranges)
        self.assertEqual(set(expected_points), set(actual_points), "Generated points with negative ranges do not match expected.")

    def test_generate_points_modulus_one(self):
        basis_matrix = [[2, 1], [1, 2]]
        modulus = 1
        lattice = Lattice(basis_matrix, modulus)
        ranges = ((0, 1), (0, 1))
        expected_points = [(0, 0), (0, 0), (0, 0), (0, 0)]
        actual_points = lattice.generate_points(*ranges)
        self.assertEqual(set(expected_points), set(actual_points), "Generated points with modulus 1 do not match expected.")

    def test_get_determinant(self):
        expected_det = 1
        actual_det = self.lattice.get_determinant()
        self.assertEqual(expected_det, actual_det, "Determinant does not match expected.")

    def test_get_determinant_non_identity(self):
        basis_matrix = [[2, 0], [0, 2]]
        lattice = Lattice(basis_matrix)
        expected_det = 4
        actual_det = lattice.get_determinant()
        self.assertEqual(expected_det, actual_det, "Determinant of non-identity matrix does not match expected.")

class TestLattice3D(unittest.TestCase):

    def setUp(self):
        self.basis_matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.lattice = Lattice(self.basis_matrix)

    def test_generate_points_3d(self):
        ranges = ((-1, 1), (-1, 1), (-1, 1))
        expected_points = [
            (-1, -1, -1), (-1, -1, 0), (-1, -1, 1),
            (-1, 0, -1), (-1, 0, 0), (-1, 0, 1),
            (-1, 1, -1), (-1, 1, 0), (-1, 1, 1),
            (0, -1, -1), (0, -1, 0), (0, -1, 1),
            (0, 0, -1), (0, 0, 0), (0, 0, 1),
            (0, 1, -1), (0, 1, 0), (0, 1, 1),
            (1, -1, -1), (1, -1, 0), (1, -1, 1),
            (1, 0, -1), (1, 0, 0), (1, 0, 1),
            (1, 1, -1), (1, 1, 0), (1, 1, 1)
        ]
        actual_points = self.lattice.generate_points(*ranges)
        self.assertEqual(set(expected_points), set(actual_points), "Generated 3D points do not match expected.")

class TestLatticeModulo(unittest.TestCase):
    def setUp(self):
        self.basis_matrix_2d = [[1, 2], [3, 4]]
        self.lattice_mod_1 = Lattice(self.basis_matrix_2d, modulus=1)

    def test_generate_points_modulus_one(self):
        ranges = ((-1, 1), (-1, 1))
        
        expected_points = [(0, 0)] * 9  
        actual_points = self.lattice_mod_1.generate_points(*ranges)
        self.assertEqual(set(expected_points), set(actual_points), "Generated points with modulus 1 do not match expected.")

    def test_get_determinant_modulus_one(self):
        expected_det_mod_1 = 0  
        actual_det_mod_1 = self.lattice_mod_1.get_determinant()
        self.assertEqual(expected_det_mod_1, actual_det_mod_1, "Determinant with modulus 1 does not match expected.")

    def test_invalid_modulus_values(self):
        with self.assertRaises(ValueError):
            Lattice(self.basis_matrix_2d, modulus=0)  
        with self.assertRaises(ValueError):
            Lattice(self.basis_matrix_2d, modulus=-1)  
        with self.assertRaises(ValueError):
            Lattice(self.basis_matrix_2d, modulus='a')  

class TestLatticeMatrix(unittest.TestCase):

    def test_generate_bad_basis(self):
        dimension = 2
        bad_basis = LatticeMatrix.generate_bad_basis(dimension)
        self.assertIn(bad_basis.det(), [1, -1], "Generated bad basis determinant is not ±1.")

    def test_generate_bad_basis_3d(self):
        dimension = 3
        bad_basis = LatticeMatrix.generate_bad_basis(dimension)
        self.assertIn(bad_basis.det(), [1, -1], "Generated bad basis determinant for 3D is not ±1.")

class TestParallelepiped2D(unittest.TestCase):

    def setUp(self):
        
        self.lattice = Lattice([[1, 0], [0, 1]])
        self.vectors = [[1, 0], [0, 1]]
        self.parallelepiped = Parallelepiped(self.lattice, self.vectors)

    def test_volume(self):
        
        expected_volume = 1  
        actual_volume = self.parallelepiped.volume()
        self.assertEqual(expected_volume, actual_volume, "Calculated volume does not match expected.")

    def test_contains_point_inside(self):
        point_inside = (0.5, 0.5)
        self.assertTrue(self.parallelepiped.contains_point(point_inside), "Point should be inside the parallelepiped.")

    def test_contains_point_outside(self):
        point_outside = (2, 2)
        self.assertFalse(self.parallelepiped.contains_point(point_outside), "Point should be outside the parallelepiped.")

    def test_contains_point_on_boundary(self):
        point_on_boundary = (1, 0)
        self.assertTrue(self.parallelepiped.contains_point(point_on_boundary), "Point on boundary should be inside the parallelepiped.")

class TestParallelepiped3D(unittest.TestCase):
    def setUp(self):
        
        self.basis_matrix_3d = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.lattice_3d = Lattice(self.basis_matrix_3d)
        self.vectors_3d = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]  
        self.parallelepiped_3d = Parallelepiped(self.lattice_3d, self.vectors_3d)

    def test_volume_3d(self):
        
        expected_volume = 1  
        actual_volume = self.parallelepiped_3d.volume()
        self.assertEqual(expected_volume, actual_volume, "3D parallelepiped volume calculation is incorrect.")

    def test_contains_point_inside_3d(self):
        
        point_inside = (0.5, 0.5, 0.5)
        self.assertTrue(self.parallelepiped_3d.contains_point(point_inside), "Point should be inside the 3D parallelepiped.")

    def test_contains_point_outside_3d(self):
        
        point_outside = (1.5, 1.5, 1.5)
        self.assertFalse(self.parallelepiped_3d.contains_point(point_outside), "Point should be outside the 3D parallelepiped.")

    def test_contains_point_on_boundary_3d(self):
        
        point_on_boundary = (1, 0, 0)
        self.assertTrue(self.parallelepiped_3d.contains_point(point_on_boundary), "Point on boundary should be considered inside the 3D parallelepiped.")

class TestLatticeValueErrors(unittest.TestCase):

    def test_basis_matrix_with_invalid_elements_raises_error(self):
        
        with self.assertRaises(ValueError):
            Lattice([[1, 'a'], [0, 1]])  
        
        
        with self.assertRaises(ValueError):
            Lattice([[1, 2], [0, 1j]])  
        
        
        with self.assertRaises(ValueError):
            Lattice([[1, None], [0, 1]])  

        
        with self.assertRaises(ValueError):
            Lattice([[1, [2]], [0, 1]])  

if __name__ == '__main__':
    unittest.main()
