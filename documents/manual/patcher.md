# Instruction guide for the LoadsKernelUtils Patcher
After installing the LoadsKernelUtils package ([installation.md](installation.md)) the patcher is directly usable in a terminal window or directly by executing the python script.
The installation of the LoadsKernelUtils package is REQUIRED for running this patcher.
Please make sure that the LoadsKernelUtils package source code includes the following folder structure:
```bash
loadskernelutils/
├── patches/
│   ├── patches.json
│   └── patches.py
...
```
These files are a prerequisite by the patcher and must include all the relevant information according to the documentation ([patcher.md](../documentation/patcher.md)).

## Starting the Patcher
The Pather can be started in two different ways.

### Starting the Patcher as a CLI command
Starting the Patcher over the terminal allows the user to directly assign a target module and to enable the export of the patching report.

#### Arguments
| Argument      | Description                                                                             | Required                             |
| ------------- | --------------------------------------------------------------------------------------- | ------------------------------------ |
| -h            | Help                                                                                    | <span style="color:blue">None</span> |
| --module_path | Path pointing to the module of where the source code that should be patched is located. | <span style="color:green">Yes</span> |
| --export      | Enables the export of the final report to the module's path.                            | <span style="color:red">No</span>    |

#### Examples
Get general information of the patcher.
```bash
user@machine:~$ LKU-setup
```

Start the patcher by assigning a module source code path.
```bash
user@machine:~$ LKU-setup --module_path ../*individual_path*/LoadsKernel
```

Request the export of the patch report. This report will be stored in the target path.
```bash
user@machine:~$ LKU-setup --module_path ../*individual_path*/LoadsKernel
```

### Starting the Patcher as a python file
When starting the patcher directly as a python file, the target code will be requested during the program flow.
An export of the patch report is currently not implemented during the manuel invokation.

## Defining new Patches
New patches can be defined by adding the code snips which should be patched in corresponding python/text files.
The patch itself is later defined in a .json file.
Inside the .json file, the input code and the targed source file is declerated.
In addition, different options can be seleceted as seen below.

#### Example
(will be revised)
Example file structure of a module:
```bash
my_project/
├── pyproject.toml
├── README.md
├── src/
│   └── example_module/
│       ├── __init__.py
│       ├── algorithms/
│       │   ├── algorithms.py           # Including the source code
│       │   ├── patch_algorithm_one.py  # Including the path of algrithm one
│       │   └── patch_algorithm_two.py  # Including the path of algrithm two
│       └── patches/
│           ├── patches.json            # Inlcuding the patch definitions
│           └── patches.py              # Including helper functions for the patcher
├── test/
└── doc/
```

Example .json file:
```bash
{
    "patches": [
        {
            "patch_name": "algorithm_one",
            "patch_type": "line",
            "patch_with_distance": false,
            "target_file": "./example_file.py",
            "patch_file": "./algorithms/patch_algorithm_one.py",
            "anchor": "import custom_module",
            "where": "before",
            "shift": 0
        },
        {
            "patch_name": "algorithm_two",
            "patch_type": "function",
            "patch_with_distance": true,
            "target_file": "./test_file.py",
            "patch_file": "./algorithms/patch_algorithm_two.py",
            "anchor": "main",
            "where": "after",
            "shift": "auto"
        }
    ]
}
```

##### Description of the pathing settings
| Name                | Description                                                                | algorithm_one                                   | algorithm_two                                     |
| ------------------- | -------------------------------------------------------------------------- | ----------------------------------------------- | ------------------------------------------------- |
| patch_type          | Selecting the searching algorithm for the anchor.                          | searching for a specific anchor line.           | Searching for a specific function body.           |
| patch_with_distance | Enables an empty row above and blow the patched part.                      | No empty lines are added.                       | Two empty lines are added.                        |
| target_file         | File on which the patching is performed.                                   | example_file.py                                 | example_file.py                                   |
| patch_file          | File that includes the code which should be patched.                       | patch_algorithm_one.py                          | patch_algorithm_two                               |
| anchor              | Specifing the anchor inside the target code.                               | "import custom_module"                          | def main(...                                      |
| where               | Defining if the patch should be performed above or below the anchor.       | The patch will be placed before the anchor row. | The patch will be placed after the function body. |
| shift               | Allows an auto shift to or a fixed space shift for the whole patched code. | The patch will be not shifted.                  | The patch will be shifted automatically.          |