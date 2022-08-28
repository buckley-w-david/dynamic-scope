__version__ = "0.1.0"

import dis
from functools import wraps
from types import FunctionType, CellType, CodeType
import inspect

_LOAD_DEREF = dis.opname.index("LOAD_DEREF")
_POP_TOP = dis.opname.index("POP_TOP")

def dynamic(f):
    """Make functions act dynamically scoped"""
    @wraps(f)
    def inner(*args, **kwargs):
        frame = inspect.currentframe()
        outer_frame = inspect.getouterframes(frame)[1]
        outer_locals = outer_frame.frame.f_locals
        outer_globals = outer_frame.frame.f_globals
        closure = []
        for name in f.__code__.co_freevars: 
            if name in outer_locals:
                closure.append(CellType(outer_locals[name])) # type: ignore
            elif name in outer_globals:
                closure.append(CellType(outer_globals[name])) # type: ignore

        return FunctionType(
            f.__code__, f.__globals__, f.__name__, f.__defaults__, tuple(closure)
        )(*args, **kwargs)
    return inner

import io
def inject(**injections):
    """Inject values into a function like it closed over them
    This usually isn't useful, except in combination with the dynamic scope decorator
    Just because something is defined in a parent scope, doesn't mean that a child scope can has a reference to it
    It needs to actually _use_ that reference for something for it to end up in it's scope (as a closure variable).
    A dynamic function called from some inner scope down the line might not have access to what you expect
    This function is meant to inject values into scopes that don't seem to otherwise use them so that dynamic scopes work"""

    def outer(f):
        c = f.__code__
        freevars = tuple([*(c.co_freevars or []), *injections.keys()])
        code = CodeType(
            c.co_argcount,
            c.co_posonlyargcount,
            c.co_kwonlyargcount,
            c.co_nlocals,
            c.co_stacksize,
            c.co_flags,
            c.co_code,
            c.co_consts,
            c.co_names,
            c.co_varnames,
            c.co_filename,
            c.co_name,
            c.co_firstlineno,
            c.co_linetable,
            freevars,
            c.co_cellvars,
        )

        closure = (*(f.__closure__ or []), *[CellType(value) for value in injections.values()]) # type: ignore
        globals = { **f.__globals__, **injections}
        return wraps(f)(FunctionType(
            code, globals, f.__name__, f.__defaults__, closure
        ))
    return outer

