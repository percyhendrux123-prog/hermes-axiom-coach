"""Load the plugin package from the repo root without Hermes installed.

The repo root is the plugin package (``__init__.py`` uses relative imports), so tests import
it under a fixed package name from the parent directory.
"""
import importlib
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PKG = "hermes_axiom_coach"


def load_plugin():
    if PKG not in sys.modules:
        spec = importlib.util.spec_from_file_location(PKG, ROOT / "__init__.py",
                                                      submodule_search_locations=[str(ROOT)])
        module = importlib.util.module_from_spec(spec)
        sys.modules[PKG] = module
        spec.loader.exec_module(module)
    pkg = sys.modules[PKG]
    for sub in ("lite.training_split", "lite.meal_plan", "lite.cardio_calc", "lite.tools", "setup_cmd"):
        importlib.import_module(f"{PKG}.{sub}")
    pkg.training_split = sys.modules[f"{PKG}.lite.training_split"]
    pkg.meal_plan = sys.modules[f"{PKG}.lite.meal_plan"]
    pkg.cardio_calc = sys.modules[f"{PKG}.lite.cardio_calc"]
    pkg.tools = sys.modules[f"{PKG}.lite.tools"]
    pkg.setup = sys.modules[f"{PKG}.setup_cmd"]
    return pkg
