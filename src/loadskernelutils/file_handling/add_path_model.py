# Setup model.hdf5 path
if hasattr(self.jcl, 'model'):
    self.path_model = data_handling.check_path(self.jcl.model['path_model'])
else:
    self.path_model = self.path_output