"""
This is a toy language interpreter/transpiler. want to translate into
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

from hindent.composing import co
from hindent.library import wrap_in_unit_function, pri, p, our_id, concat, t
from hindent.hindent_parser import translate_hindent



x = wrap_in_unit_function(1)
y = wrap_in_unit_function(2)
hey = wrap_in_unit_function("hey ")
there = wrap_in_unit_function("there ")
fam = wrap_in_unit_function("fam")

newlang_code = """

} pri
  } p
    x
    } p
      x
      y

"""

eval(translate_hindent(newlang_code))

newlang_code_2 = """

} } pri
    } concat
      hey
      there
  } pri
    } concat
      hey
      } concat
        there
        fam
  } pri
    } t
      } p
        x
        y
      } p
        x
        y

"""

eval(translate_hindent(newlang_code_2))
