import importlib
from pathlib import Path

INIT_FILE_NAME = "__init__.py"


def create_init_files(module_name: str):
    module_path = Path(importlib.util.find_spec(module_name).origin)
    for path_object in module_path.parent.rglob("*"):
        if path_object.is_dir():
            init_file_path = path_object / INIT_FILE_NAME
            if not init_file_path.exists():
                print(f"init file not exist: {init_file_path}")
                open(init_file_path, "a").close()


def import_attr(full_path: str):
    """Given a full import path to a module attr, return the imported attr.

    For example, the following are equivalent:
        MyClass = import_attr("module.submodule:MyClass")
        MyClass = import_attr("module.submodule.MyClass")
        from module.submodule import MyClass

    Returns:
        Imported attr
    """
    if full_path is None:
        raise TypeError("import path cannot be None")

    if ":" in full_path:
        if full_path.count(":") > 1:
            raise ValueError(
                f'Got invalid import path "{full_path}". An '
                "import path may have at most one colon."
            )
        module_name, attr_name = full_path.split(":")
    else:
        last_period_idx = full_path.rfind(".")
        module_name = full_path[:last_period_idx]
        attr_name = full_path[last_period_idx + 1 :]

    create_init_files(module_name)
    module = importlib.import_module(module_name)
    return getattr(module, attr_name)


# print(import_attr(full_path="hello_serve:model"))

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, 'utils')

import test

# Import the module.
hello = test.hello


module = importlib.import_module("hello_serve")
print(module)


# import importlib
# module_name = 'test_anyscale_deployments.utils_repro.hello_serve'
# path = Path(importlib.util.find_spec(module_name).origin)
#
# init_file_name = "__init__.py"
# for path_object in path.parent.rglob("*"):
#     if path_object.is_dir():
#         print(path_object.name)
#         init_file_path = path_object / init_file_name
#         if not init_file_path.exists():
#             print(f"init file not exist: {init_file_path}")
#
# importlib.util.find_spec('test_anyscale_deployments.utils_repro.hello_serve').origin
# importlib.import_module('test_anyscale_deployments.utils_repro.hello_serve')