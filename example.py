from dynamic_scope import dynamic, inject
import dis
import inspect


# def f():
#     spam = "test"

#     def g():
#         print(spam)

#     @dynamic
#     def h():
#         print(spam)

#     return g, h

# def g():
#     spam = "Hello, World!"

#     @inject(spam=spam)
#     def inner():
#         _, dynamic = f()
#         dynamic()
    
#     return inner

# i = g()

# def make_function():
#     value = 0
#     @dynamic
#     def g():
#         return value
#     return g

# def use_function():
#     value = 1
#     @inject(value=value)
#     def inner():
#         dyn = make_function()
#         return dyn()
#     return inner()

def g():
    spam = "Hello, World!"
    @dynamic
    def t1():
        return spam
    return t1

def h():
    spam = "Goodbye, World!"
    @inject(spam=spam)
    def inner():
        t = g()
        return t()
    return inner()

i = h()
print(i)
"""
f.__code__.co_freevars is empty
f.__code__.co_cellvars are the variables g closes that we pass down (x)

g.__code__.co_freevars are the variables g closes over from f (x)
g.__code__.co_cellvars are the variables g defines and passes down h (y)

h.__code__.co_freevars are the variables h closes over from f and g
h.__code__.co_cellvars is empty

func.__closure__ are cell references (loaded by LOAD_DEREF) for func.__code__.co_freevars

To replace a closure, I believe you just have to replace __closure__. I am not sure if it is important to replace co_freevars as well, or co_cellvars  from the parent scope

This might screw with further nested scopes. No clue

def f():
    x = 5
    def g():
        y = 6
        def h():
            return x, y
        print(h.__code__.co_freevars)
        print(h.__code__.co_cellvars)
        print(h.__closure__)
        print(locals())
        breakpoint()
        return h
    print(g.__code__.co_freevars)
    print(g.__code__.co_cellvars)
    print(g.__closure__)
    print(locals())
    # breakpoint()
    return g
f()

  4           0 LOAD_CONST               1 (5)
              2 STORE_DEREF              0 (x)

  5           4 LOAD_CLOSURE             0 (x)
              6 BUILD_TUPLE              1
              8 LOAD_CONST               2 (<code object g at 0x7fea728b5d10, file "/home/david/Projects/dynamic-scope/example.py", line 5>)
             10 LOAD_CONST               3 ('f.<locals>.g')
             12 MAKE_FUNCTION            8 (closure)
             14 STORE_FAST               0 (g)

 14          16 LOAD_GLOBAL              0 (print)
             18 LOAD_FAST                0 (g)
             20 LOAD_ATTR                1 (__code__)
             22 LOAD_ATTR                2 (co_freevars)
             24 CALL_FUNCTION            1
             26 POP_TOP

 15          28 LOAD_GLOBAL              0 (print)
             30 LOAD_FAST                0 (g)
             32 LOAD_ATTR                1 (__code__)
             34 LOAD_ATTR                3 (co_cellvars)
             36 CALL_FUNCTION            1
             38 POP_TOP

 16          40 LOAD_GLOBAL              0 (print)
             42 LOAD_FAST                0 (g)
             44 LOAD_ATTR                4 (__closure__)
             46 CALL_FUNCTION            1
             48 POP_TOP

 17          50 LOAD_GLOBAL              5 (breakpoint)
             52 CALL_FUNCTION            0
             54 POP_TOP

 18          56 LOAD_FAST                0 (g)
             58 RETURN_VALUE

Disassembly of <code object g at 0x7fea728b5d10, file "/home/david/Projects/dynamic-scope/example.py", line 5>:
  6           0 LOAD_CONST               1 (6)
              2 STORE_DEREF              0 (y)

  7           4 LOAD_CLOSURE             1 (x)
              6 LOAD_CLOSURE             0 (y)
              8 BUILD_TUPLE              2
             10 LOAD_CONST               2 (<code object h at 0x7fea728b54d0, file "/home/david/Projects/dynamic-scope/example.py", line 7>)
             12 LOAD_CONST               3 ('f.<locals>.g.<locals>.h')
             14 MAKE_FUNCTION            8 (closure)
             16 STORE_FAST               0 (h)

  9          18 LOAD_GLOBAL              0 (print)
             20 LOAD_FAST                0 (h)
             22 LOAD_ATTR                1 (__code__)
             24 LOAD_ATTR                2 (co_freevars)
             26 CALL_FUNCTION            1
             28 POP_TOP

 10          30 LOAD_GLOBAL              0 (print)
             32 LOAD_FAST                0 (h)
             34 LOAD_ATTR                1 (__code__)
             36 LOAD_ATTR                3 (co_cellvars)
             38 CALL_FUNCTION            1
             40 POP_TOP

 11          42 LOAD_GLOBAL              0 (print)
             44 LOAD_FAST                0 (h)
             46 LOAD_ATTR                4 (__closure__)
             48 CALL_FUNCTION            1
             50 POP_TOP

 12          52 LOAD_GLOBAL              5 (breakpoint)
             54 CALL_FUNCTION            0
             56 POP_TOP

 13          58 LOAD_FAST                0 (h)
             60 RETURN_VALUE

Disassembly of <code object h at 0x7fea728b54d0, file "/home/david/Projects/dynamic-scope/example.py", line 7>:
  8           0 LOAD_DEREF               0 (x)
              2 LOAD_DEREF               1 (y)
              4 BUILD_TUPLE              2
              6 RETURN_VALUE
"""
