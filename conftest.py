import pkgutil
import sys

_orig_resolve = pkgutil.resolve_name

def _resolve_name_tolerant(name):
    try:
        return _orig_resolve(name)
    except ValueError:
        # Python 3.14 pkgutil.resolve_name rejects names with hyphens.
        # Fall back to direct sys.modules lookup so unittest.mock.patch
        # can target modules loaded from hyphenated directory names.
        if name in sys.modules:
            return sys.modules[name]
        if "." in name:
            mod_name, attr = name.rsplit(".", 1)
            mod = sys.modules.get(mod_name)
            if mod is not None:
                return getattr(mod, attr)
        raise

pkgutil.resolve_name = _resolve_name_tolerant
