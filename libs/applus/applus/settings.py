# -*- coding: utf-8 -*-
""" 可配置变量 """
from importlib import import_module


_SETTING_REGISTERED = "The '{}' {} setting has been registered, can not occur in '%s'."
_SETTING_SET = "The '%s' %s setting has been set."
_SETTING_REMOVED = "The '%s' %s setting has been removed."
_INVALID_SETTING = "Invalid %s setting: '%s'"

_IMPORT_ERROR = "Could not import '%s' for %s setting '%s': %s"
_PATH_ERR = "doesn't look like a module path"
_ATTR_ERR = "module doesn't define the attribute/class"


def perform_import(dotted_path, namespace, attr):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
        module = import_module(module_path)
    except (ValueError, ModuleNotFoundError) as err:
        raise ImportError(_IMPORT_ERROR % (
            dotted_path, namespace, attr, _PATH_ERR)) from err

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError(_IMPORT_ERROR % (
            dotted_path, namespace, attr, _ATTR_ERR)) from err


def _clean(value, func_or_name, namespace, attr):
    """ perform clean operation on value. """
    if not func_or_name:
        return value
    if callable(func_or_name):
        return func_or_name(value)
    func = perform_import(func_or_name, namespace, attr)
    return func(value)


class Settings:
    """ A settings object, that allows settings to be accessed as properties.
    For example:

        from applus.settings import Settings
        settings = Settings("API")
        print(api_settings.VERSION)

    Any setting with string import paths will be automatically resolved
    and return the class, rather than the string literal.
    """
    def __init__(self, namespace):
        self.namespace = namespace.upper()
        self.user_settings = {}
        self.defaults = {}
        self.import_strings = []
        self.clean_settings = {}
        self.removed_settings = []
        self._cached_attrs = set()

    def extend(self, defaults, import_strings, clean_settings, removed_settings):
        """ 扩展配置空间 """
        for setting in self.defaults:
            msg = _SETTING_REGISTERED.format(setting, self.namespace)
            if setting in defaults:
                raise RuntimeError(msg % 'DEFAULTS')
            if setting in import_strings:
                raise RuntimeError(msg % 'IMPORT_STRINGS')
            if setting in clean_settings:
                raise RuntimeError(msg % 'CLEAN_SETTINGS')
            if setting in removed_settings:
                raise RuntimeError(msg % 'REMOVED_SETTINGS')
        self.defaults.update(defaults)
        self.import_strings.extend(import_strings)
        self.clean_settings.update(clean_settings)
        self.removed_settings.extend(removed_settings)

    def update(self, user_settings=None):
        """ 扩展配置 """
        if not user_settings:
            return
        for setting in user_settings:
            if setting in self.user_settings:
                raise RuntimeError(_SETTING_SET % (
                    setting, self.namespace))
            if setting in self.removed_settings:
                raise RuntimeError(_SETTING_REMOVED % (
                    setting, self.namespace))
        self.user_settings.update(user_settings)

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError(_INVALID_SETTING % (
                self.namespace, attr))

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, self.namespace, attr)

        # Clean value
        if attr in self.clean_settings:
            val = _clean(val, self.clean_settings[attr], self.namespace, attr)

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def clear(self, clear_settings):
        """ 清空缓存，或用户配置 """
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if clear_settings:
            self.user_settings.clear()
