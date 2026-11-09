from pathlib import Path

def get_patches() -> Path:
    return Path(__file__).parent / "patches.json"

def get_patch_file(rel_path) -> Path:
    return Path(__file__).parent / rel_path

def get_package_dir() -> Path:
    return Path(__file__).parent.parent