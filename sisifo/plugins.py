# Import with "_" to avoid polluting "plugins" module.
import importlib as _importlib
import logging as _logging
import os as _os
import pkgutil as _pkgutil


def _find_plugins():
    plugins = {}
    for _, full_name, _ in _pkgutil.iter_modules():
        if full_name.startswith("sisifo_"):
            _, name = full_name.split("_")
            plugins[name] = full_name
    return plugins


def _import_plugin(full_name):
    try:
        return _importlib.import_module(full_name)
    except Exception:
        _logging.exception(f"Cannot import sisifo plugin '{full_name}'")


def _import_plugins(plugins):

    imported_plugins = {}
    for name, full_name in plugins.items():
        module = _import_plugin(full_name)
        if module:
            imported_plugins[name] = module
    return imported_plugins


def _append_to_current_module(imported_plugins):
    for name, module in imported_plugins.items():
        globals()[name] = module


def load_plugins():
    plugins = _find_plugins()
    imported_plugins = _import_plugins(plugins)
    _append_to_current_module(imported_plugins)


def _load_plugins_start_up():
    if "SISIFO_NO_PLUGINS" not in _os.environ:
        load_plugins()


_load_plugins_start_up()
