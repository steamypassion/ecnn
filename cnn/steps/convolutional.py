import numpy as np
from cnn.common import get_array
from cnn.steps.activation import Linear
from cnn.steps.basic import StepWithFilters


class ConvolutionalStep(StepWithFilters):
    '''
    feature_size: tuple (height widht) or (width) for 1 dimentianl array
    x0: initiale features values (random, ones, zeros)
    padding: number for equels
    '''

    def __init__(self, filter_size, num_of_kernels, activation=Linear, x0='random', padding=None,
                 stride=1):
        super().__init__(activation)

        self.num_of_filters = num_of_kernels
        self.filter_size = filter_size
        self.x0 = x0
        self.padding = padding
        self.activation = activation

        self.stride = stride

    def back_prop(self, delta, leraning_rate=0.001):
        errors = []
        f = np.array(self.filters)
        old_shape = f.shape
        fltten = f.reshape((f.shape[0], f.shape[1] * f.shape[2] * f.shape[3]))

        delta_sum = np.sum(delta)
        for filter in self.filters:
            filter_error = 0
            # filter += delta[i]
            # neuron_weights = fltten[i, :]
            filter_gradiant = (delta * self.activation.back_propagation(self.z).reshape(self.z.size)).dot(leraning_rate)
            graidnat_sum = np.sum(filter_gradiant)

            filter += graidnat_sum
            # neuron_error = np.sum(filter_gradient) * self.activation.derivative(self.z)
            errors.append(graidnat_sum)

        return errors

    def calc_neurons_values(self, input):
        input = self.__add_padding(input)

        if self.filters is None:
            self.filters = self.__initiliaze_features(input.shape)

        feature_height, feature_widht = self.filters[0].shape[1], self.filters[0].shape[2]
        bulks = self.__get_sub_arrays(input, self.stride, (feature_height, feature_widht))

        features_sum_of_products = []

        for feature in self.filters:
            features_sum_of_products.append(
                [[self.__get_bulk_sum_of_products(bulk, feature) for bulk in row] for row in bulks])

        return np.stack(features_sum_of_products, axis=0)

    def __add_padding(self, input):
        if self.padding is None:
            return input

        if input.shape[1] == 1:
            padding_size = [(0, 0)] * 2 + [(self.padding, self.padding)]
        else:
            padding_size = [(0, 0)] + [(self.padding, self.padding)] * 2

        return np.lib.pad(input, padding_size, 'constant')

        # return input

    def __get_bulk_sum_of_products(self, bulk, feature):
        multiplied = feature * bulk
        return np.sum(np.reshape(multiplied, multiplied.size))

    def __initiliaze_features(self, input_shape):
        feature_size = (input_shape[0],)

        if isinstance(self.filter_size, tuple):
            filter_height = self.filter_size[0]
            filter_width = self.filter_size[1]
        else:
            filter_height = filter_width = self.filter_size

        feature_size += (min(filter_height, input_shape[1]), min(filter_width, input_shape[2]))

        return [get_array(self.x0, feature_size) for i in range(self.num_of_filters)]

    def __get_sub_arrays(self, input, stride, size):
        input_height, input_width = input.shape[1], input.shape[2]
        size_height = size[0]
        size_width = size[1]

        bulks = []

        for i in range(0, input_height, stride):
            row = []
            if i + size_height > input_height:
                continue

            for j in range(0, input_width, stride):
                if j + size_width > input_width:
                    continue

                # bulk = input[:, i: input_width, j: j + feature_widht]
                # else:
                bulk = input[:, i: i + size_height, j: j + size_width]
                row.append(bulk)

            bulks.append(row)

        return bulks