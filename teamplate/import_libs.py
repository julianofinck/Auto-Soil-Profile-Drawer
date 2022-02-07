def install_if_nonexistent(module_name, install_name='same_name'):
    if install_name == 'same_name':
        install_name = module_name
    from importlib import util
    if util.find_spec(module_name) is not None:
        print('Module already installed: ' + module_name)
        pass
    else:
        import os
        print('Installing new module... Aguarde\n' + module_name + '\n\n')
        os.system('python -m pip install ' + install_name)

