        
# Setup individual control surface actuation
if hasattr(self.jcl.efcs, 'keys'):
    for i, cs in enumerate(self.jcl.efcs['keys']):
        self.inputs = np.vstack((
            self.inputs,
            np.array([f'cs_{cs}', 'fix', 0.0], dtype=object),
        ))