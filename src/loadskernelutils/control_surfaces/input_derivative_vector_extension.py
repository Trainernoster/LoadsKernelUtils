
# Setup individual control surface actuation
if 'keys' in self.jcl.efcs:
    for i, cs in enumerate(self.jcl.efcs['keys']):
        self.input_derivatives = np.vstack((
            self.input_derivatives,
            np.array([f'cs_{cs}', 'fix', 0.0], dtype=object),
        ))