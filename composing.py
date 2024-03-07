from functools import partial
import inspect


# Function to calculate remaining arguments, now handles both partials and regular functions
def remaining_args(func_or_partial):
    # Check if the input is a partial object
    if isinstance(func_or_partial, partial):
        # If so, retrieve the original function and count the supplied arguments
        original_func = func_or_partial.func
        supplied_args_count = len(func_or_partial.args) + len(func_or_partial.keywords)
    else:
        # If it's not a partial, it's a regular function, so consider no arguments supplied
        original_func = func_or_partial
        supplied_args_count = 0
    
    # Inspect the original function signature
    sig = inspect.signature(original_func)
    total_params = len(sig.parameters)
    
    # Calculate remaining arguments required
    remaining = total_params - supplied_args_count
    return remaining

def co(*fs):

    if len(fs) == 0:
        raise Exception("No functions to compose")
    
    if len(fs) == 1:
        return fs[0]
    
    for i, f in enumerate(fs):

        if i == 0:
            current = f

        if remaining_args(current) == 1:

            return current(fs[i+1])
        else:
            current = partial(current, fs[i+1])

    # this happens if the function accepts more arguments than 
    # the number of functions to compose
    return current
