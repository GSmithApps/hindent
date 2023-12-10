Hindent is a syntax wrapper around lisp/scheme.
The difference between Hindent and lisp/scheme is very simple:
wherever lisp/scheme uses parenthesis,
Hindent uses hanging indents.  For example:

```
# Hindent

+
  2
  2

# lisp

(+ 2 2)
```

And some more examples:

```
display
  +
    2
    2

(display (+ 2 2))
```

```
display
  car
    quote
      1
        2
        3

(display (car (quote (1 2 3))))
```

```
define
  x
  4

+
  2
  x

(define x 4)
(+ 2 x)
```

# How it works

Hindent simply parses the Hindent code and
inserts parenthesis where appropriate to convert
it to lisp/scheme.  So, it is mostly
a parser, but a fancy word for it could be a transpiler.

# Installation

1. `pip install hindent`
2. Install chez scheme (`brew install chezscheme`)
   and make sure it's on your path by running `chez`.
   - This also works with other lisps or schemes. If
     you want to do that, the
     notes in the ``initialize`` method will explain how
     to do it.
3. The syntax highlighter for vs code is
   [`Hindent Lang`](https://marketplace.visualstudio.com/items?itemName=GrantSmith.hindent-lang)

# Usage

I think a nice way to interactively run programs is with jupyter.
So, I recommend opening up a jupyter notebook. Then, simply start to
import ``Hindent`` with `from Hindent`, and the docstrings/code-hover
will guide you from there.

> One heads up is that when running, the `newline` and `display` functions
> are helpful.  If you don't use `display`, then lisp will not output
> anything. So, if you are experimenting, and you want to see results
> of what you run, you need to use `display`.
> And regarding `newline`, if you don't use it, all of the output will be smushed
> together.


# Parsing Spec

- the transpiler supports literate programming. So, most of the
  source code is natural language.
  - to denote a block of code, it will be similar to how markdown
    does it, but instead of three backticks, it is a lone period.
    So basically, a lone period on a line toggles between
    natural language and code (starting with natural language).
- the parser/transpiler will put a new line after the source code
  to ensure the final dedent is correct
- any amount of whitespace that contributes to a blank line
  (other than the last line) should be replaced with a single
  new line character. For example, `\n\n\n` should be replaced
  with `\n`, and `\n   \n` should also be replaced with `\n`
- lines that start with `;` are comments and will be ignored
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

- [ ] VS Code extension
  - [ ] file icon
  - [ ] syntax highlight code vs comments/natural language
- [ ] allow for end-of-line comments
- [ ] maybe get it out of running as a subprocess so
      it returns things more easily
- [ ] make a sphinx site
  - [ ] convert readme to rst (change in pyproject.toml as well)
- [ ] make into a package and push to conda

# Notes For Grant

`flit build --format wheel`
`twine upload dist/*`
