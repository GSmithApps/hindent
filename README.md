Hindent is a syntax wrapper around lisp/scheme.
The difference between Hindent code and lisp/scheme code is very simple:
wherever lisp/scheme uses parenthesis,
Hindent uses hanging indents.

To do this, Hindent simply parses the Hindent code and
inserts parenthesis where appropriate.  So, it is mostly
a parser, but a fancy word for it could be a transpiler.
To use it as a transpiler, simply call the ``transpile``
method.

It also allows you to run the code if you have a lisp/scheme
interpreter installed.  It defaults to chez scheme, but you
can change it to any lisp/scheme interpreter you want by
simply passing a callable to the ``initialize`` method.
Then you can run with the ``execute_lisp`` method.

# Example hindent code

```
display
  +
    2
    2

newline

display
  car
    quote
      1
        2
        3

define
  x
  4

newline

display
  +
    2
    x

```

# Installation

1. Clone this repository or simply grab the python file
2. Install chez scheme and make sure it's on your
   path by running `chez`.
   - This also works with other lisps or schemes. If
     you want to do that, the
     notes in the ``initialize`` method will explain how
     to do it.

# Usage

I think a nice way to interactively run programs is with jupyter.
So, I recommend opening up a jupyter notebook. Then, simply start to
import ``Hindent`` with `from Hindent`, and the docstrings/code-hover
will guide you from there.



# Parsing Spec

- the first line should have no indents
- the last line should be blank
- any amount of whitespace that contributes to a blank line
  (other than the last line) should be replaced with a single
  new line character. For example, `\n\n\n` should be replaced
  with `\n`, and `\n   \n` should also be replaced with `\n`
- calculate the number of spaces each line starts with.
- Then divide by 2 to determine the indentation level
- then, for each line find the difference in indentation level
  between that line and the following line
  - if the indentation level goes up one, then add an opening parenthesis before the line
  - if the indentation level goes down, then add a closing parenthesis after the line
    according to the number of dedents.
  - if the indentation level remains the same, then we have to check one more thing:
    - if the current indentation level (and also the indentation level of the following line)
      is at 0, then wrap the current line in parenthesis
    - if the current indentation level (and also the indentation level of the following line)
      is nonzero, then do nothing

# ToDo

- [ ] allow for comments
  - [ ] actually, reverse code and comments to allow
        for literate programming
- [ ] VS Code extension
  - [ ] file icon
  - [ ] syntax highlight comments
