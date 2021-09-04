import sisifo


def test_find_plugins(mocker):
    mocker.patch("pkgutil.iter_modules", return_value=[
        (None, "sisifo_myplugin", None),
        (None, "other_package", None),
    ])
    assert sisifo.namespaces._find_plugins() == {"myplugin": "sisifo_myplugin"}


def test_import_plugins(mocker):
    import_module_mock = mocker.patch("importlib.import_module")
    plugins = {"myplugin": "sisifo_myplugin"}
    imported_plugins = sisifo.namespaces._import_plugins(plugins)
    import_module_mock.assert_called_once_with("sisifo_myplugin")
    assert imported_plugins == {"myplugin": import_module_mock()}


def test_import_plugins_with_errors(mocker):
    import_module_mock = mocker.patch("importlib.import_module")
    import_module_mock.side_effect = ["module_ok_loaded", Exception()]
    plugins = {"myplugin1": "module_ok", "myplugin2": "module_with_errors"}
    imported_plugins = sisifo.namespaces._import_plugins(plugins)
    assert imported_plugins == {"myplugin1": "module_ok_loaded"}


def test_do_not_load_plugins_on_start_up(mocker):
    mocker.patch.dict("os.environ", {"SISIFO_NO_PLUGINS": ""})
    find_plugins_mock = mocker.patch("sisifo.namespaces.load_plugins")
    sisifo.namespaces._load_plugins_start_up()
    assert not find_plugins_mock.called
