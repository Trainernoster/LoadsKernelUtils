# Installation guide for the LoadsKernelUtils Package

## Short information about the LoadsKernelUtils (LKU) Package
The LoadsKernelUtils package is developt to supply additional code for the LoadsKernel developt by the DLR.
Included in this python package is a patching software which is automatically installed during the following process.
This software script patches all relevant changes directly and automatically in the LoadsKernel's source code.
A detailed description of the patcher can be found in [manual/patcher.md](../manual/patcher.md) and [documents/patcher.md](../documents/patcher.md) .

## Installing the LKU Package
This package is designed to be used in python environments managed by pip.
Therefore it can be installed directly to the environments library collector or as an editable installation.

### Direct installation
The following listing shows the direct installation to the library collector.
```
cd ../LoadsKernelUtils
pip install .
```

### Editable installation
The following listing shows the editable installation
```
cd ../LoadsKernelUtils
pip install -e .
```
If the editable installation will lead to an folder structure error under pip try:
(The module can not be found in the python environment's library. It only can be included by adding the package root folder. This error happends in newer pip versions)
```
pip install -e . --config-settings editable_mode=compat
```