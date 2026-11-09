...

### patcher.py file

This file must include the following code.
It is required such that the patcher can request the correct input paths.

```bash
from pathlib import Path

def get_patches() -> Path:
    return Path(__file__).parent / "patches.json"

def get_package_dir() -> Path:
    return Path(__file__).parent.parent
```
The function **get_patches** returns the .json file in which the patches are defined.
It includes the instructions for the patcher.
The function **get_package_dir** returns the root directory of the moodule including the new code snips.