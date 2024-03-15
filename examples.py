"""
This is a toy language interpreter/transpiler. It translates
the toy code into
a snippet of specialized python code. The basic idea is to
use indentation and curly braces `}` to denote nested parenthesis
and a call to a `compose` function. For example, I want

```newlang
} my_func
  2
  2
```

to be converted to

```python
compose(myfunc, 2, 2,)
```

and with nesting, we want

```newlang
} newfunc
  2
  } otherfunc
    3
    4
```

to be

```python
compose(newfunc, 2, compose(otherfunc, 3, 4,),)
```
"""

from hindent import co, translate_hindent, wrap_in_unit_function, pri, p, our_id, concat, t, run_hindent
# from hindent.library import wrap_in_unit_function, pri, p, our_id, concat, t
# from hindent.library import *


x = wrap_in_unit_function(1)
y = wrap_in_unit_function(2)
hey = wrap_in_unit_function("hey ")
there = wrap_in_unit_function("there ")
fam = wrap_in_unit_function("fam")


newlang_code = """

} print
  } +
    x
    } +
      x
      y

"""

run_hindent(newlang_code, locals())

newlang_code_2 = """

} } print
    } concat
      hey
      there
  } print
    } concat
      hey
      } concat
        there
        fam
  } print
    } *
      } +
        x
        y
      } +
        x
        y

"""

run_hindent(newlang_code_2, locals())
