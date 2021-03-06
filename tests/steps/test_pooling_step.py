import unittest
import numpy as np
from cnn.steps import MaxPoolingStep


class PoolingActivationTests(unittest.TestCase):
    def test_max_pooling_1d_array(self):
        # arrange
        input = np.array([[[1, 2, -3, 4]]])
        expected = np.array([[[2, 4]]])
        pooling = MaxPoolingStep(2)

        # act
        output = pooling.forward_propagation(input)

        # assert
        self.assertEqual(expected.shape, output.shape)
        self.assertTrue(all(np.equal(expected.reshape(expected.size), output.reshape(output.size))))

    def test_max_pooling_2d_array(self):
        input = np.array([[
            [4, 5, 7, 2, 8, 5],
            [3, 5, 7, 82, 35, 4],
            [-3, -7, 23, 6, 2, 0],
            [-98, 23, 59, -23, 0, 2],
            [1, 2, 3, 4, 5, 6],
            [-7, -6, -2, 7, 0.45, 2]
        ]])
        expected = np.array([[
            [5, 82, 35],
            [23, 59, 2],
            [2, 7, 6]
        ]])
        pooling = MaxPoolingStep(2)

        # act
        output = pooling.forward_propagation(input)

        # assert
        self.assertEqual(expected.shape, output.shape)
        self.assertTrue(all(np.equal(expected.reshape(expected.size), output.reshape(output.size))))

    def test_max_pooling_3d_array(self):
        input = np.array([
            [
                [1, 2, 3],
                [4, 3, 2, ],
                [7, -4, 7],
            ],
            [
                [0, -23, 100],
                [2, 5, 6],
                [-23.9, 4, 20.7]
            ]
        ])
        expected = np.array([[[7]], [[100]]])
        pooling = MaxPoolingStep(3)

        # act
        output = pooling.forward_propagation(input)

        # assert
        self.assertEqual(expected.shape, output.shape)
        self.assertTrue(all(np.equal(expected.reshape(expected.size), output.reshape(output.size))))

    def test_pooling_saves_z_with_0_for_unpooled(self):
        input = np.array([[
            [4, 5, 7, 2, 8, 5],
            [3, 5, 7, 82, 35, 4],
            [-3, -7, 23, 6, 2, 0],
            [-98, 23, 59, -23, 0, 2],
            [1, 2, 3, 4, 5, 6],
            [-7, -6, -2, 7, 0.45, 2]
        ]])
        expected_z = [
            0, 1, 0, 0,
            0, 0, 0, 1,
            0, 0, 1, 0,
            0, 0, 0, 1,
            0, 0, 1, 0,
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 0, 1,
            0, 1, 0, 0
        ]

        pooling = MaxPoolingStep(2)

        # act
        output = pooling.forward_propagation(input)

        # assert
        self.assertEqual(len(expected_z), len(pooling.z))
        self.assertEquals(expected_z, pooling.z)

    def test_pooling_back_drop(self):
        # arrange
        error = 6
        inputs = np.array([[
            [7, 8],
            [0, 2]
        ]])
        expected = np.array([[
            [0, error],
            [0, 0]
        ]])

        pooling = MaxPoolingStep(2)
        output = pooling.forward_propagation(inputs)

        # act
        backdrop = pooling.back_prop(np.array([error]), None)

        # assert
        self.assertEqual(expected.shape, backdrop.shape)
        self.assertTrue(all(np.equal(expected.reshape(expected.size), output.reshape(backdrop.size))))

