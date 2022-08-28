from dynamic_scope import __version__

from dynamic_scope import dynamic, inject

def test_dynamic_scope():
    def make_functions():
        # value has to be defined locally in a parent scope
        # otherwise the generated bytecode in the functions will treat it
        # as a global
        value = 0

        def normal():
            return value

        @dynamic
        def dyn():
            return value

        return normal, dyn

    value = 1
    normal, dyn = make_functions()
    assert normal() == 0
    assert dyn() == 1

    value = 2
    assert normal() == 0
    assert dyn() == 2

def test_inject():
    def make_function():
        value = 0
        @dynamic
        def g():
            return value
        return g

    def use_function():
        value = 1
        @inject(value=value)
        def inner():
            dyn = make_function()
            return dyn()
        return inner()

    assert use_function() == 1
