import importlib
import pkgutil

import auction_lens


def test_all_modules_import():
    for module in pkgutil.walk_packages(auction_lens.__path__, "auction_lens."):
        importlib.import_module(module.name)
