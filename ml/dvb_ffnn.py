from keras import Sequential
from keras.layers import Dense, Activation
import numpy as np


class Encoding:

    @staticmethod
    def get_n_bits(n_values):
        return np.ceil(np.log2(n_values))


class DvbFfnn:

    def __init__(self, n_line_direction_id, n_weather_types, max_late_early_time, n_weeks=52, n_weekdays=7, n_hours=12, n_temp_vals=1, dim_locations = 2):
        self.n_inputs = sum([
            Encoding.get_n_bits(n_weeks),  # binary encoded
            Encoding.get_n_bits(n_weekdays),  # binary encoded
            Encoding.get_n_bits(n_hours),  # binary encoded
            n_temp_vals,  # 1.0 / n_temp_vals
            Encoding.get_n_bits(n_weather_types),  # binary encoded
            Encoding.get_n_bits(n_line_direction_id),  # binary encoded
            dim_locations  # n_locations = 1 / n_delta_lat, 1 / n_delta_lon,
        ])

        self.input_layer = Dense(self.n_inputs)
        self.h1 = Dense(self.n_inputs + 1)
        self.output_layer = Dense(Encoding.get_n_bits(max_late_early_time))

        self.model = Sequential(
            [
                self.input_layer,
                Activation("relu"),
                self.h1,
                Activation("relu"),
                self.output_layer
            ]
        )

        pass
