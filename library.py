from typing import Any, Callable, Union

def wrap_in_unit_function(x) -> Callable[[None], Any]:
    """
    Raise a value to be a function
    """
    def returnfunc(y):
        if y is None:
            return x
        else:
            raise NotImplementedError("This function's domain is None")

    return returnfunc

def our_id(f: Callable[[Any], None]) -> Callable[[Any], None]:
    """
    The identity function.

    This works on functions or on values. 
    - If it's given a function, it returns the function.
    - If it's given a value, it returns that value.
    """

    return f

Numeric = Union[int, float, complex]

def p(f1_num: Callable[[None], Numeric],f2_num: Callable[[None], Numeric]) -> Callable[[None], Numeric]:
    """
    Plus on the level of functions
    """

    return wrap_in_unit_function(f1_num(None) + f2_num(None))


def pri(f: Callable[[None], Any]) -> Callable[[Callable[[Any],None]], Callable[[Any],None]]:
    """
    print on the level of functions
    """
    print(f(None))
    return our_id

def concat(f1_string: Callable[[None], str],f2_string: Callable[[None], str]) -> Callable[[None], str]:
    """
    Concatenation on the level of functions
    """

    return wrap_in_unit_function(f1_string(None) + f2_string(None))

