Hindent is a syntax wrapper around lisp/scheme.
The difference between Hindent and lisp/scheme is very simple:
wherever lisp/scheme uses parenthesis,
Hindent uses hanging indents.  For example:

```
; Hindent

+
  2
  2

; lisp

(+ 2 2)

; example.hin has more examples
```

# Example

> **Example code: `example.hin`**

The easiest way to think about it
is to repeat the following:

- Focus on the the deepest nesting
  level. This is the current chunk.
- Follow the chunk upward and leftward
  to where the nearest dedent
  is, which we call the lead.
- Collapse the chunk's newlines
  and indentation,
  wrap it in parenthesis,
  and leave it where the lead was. 
 
Let's do an example step-by-step

```
+
  -
    4
    1
  2
```

Focus on the part with deepest nesting.
In this case, it is the `4` and `1`.
Then track upwards to find the
lead, which is `-`.
Then collapse, wrap in parenthesis, and
leave it where the lead was.

```
+
  (- 4 1)
  2
```

Do it again. Focus on the deepest
nesting. In this case, it is
`(- 4 1)` and `2`.  Follow
upward and to the left to find
the lead, which is `+`.  Collapse,
wrap in parenthesis, and leave
where the lead was

```
(+ (- 4 1) 2)
```

# How it works

Hindent simply parses the Hindent code and
inserts parenthesis where appropriate to convert
to lisp/scheme.  So, it is mostly
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
   [`Hindent Lang`](https://marketplace.visualstudio.com/items?itemName=GrantSmith.hindent-lang).  You can find
   it in the normal extensions menu / marketplace.

# Usage

I think a nice way to interactively run programs is with jupyter.
So, I recommend opening up a jupyter notebook. Then, simply start to
import ``Hindent`` with `import Hindent as h`, and the docstrings/code-hover
will guide you from there.

> One heads up is that when running, the `newline` and `display` functions
> are helpful.  If you don't use `display`, then lisp will not output
> anything. So, if you are experimenting, and you want to see results
> of what you run, you need to use `display`.
> And regarding `newline`, if you don't use it, all of the output will be smushed
> together.


# Parsing Spec

- the transpiler supports literate programming. It does so
  by putting block comments on equal footing with code. To
  toggle back and forth between code and block comment,
  put a lone period on a line.
  - For reasons of textmate grammars and syntax highlighting,
    we had to make the file start as code, rather than starting
    as block comment. We would have preferred it the other way,
    but we think it's okay.  We're thankful for how awesome vs
    code and textmate are.
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

- [ ] maybe get it out of running as a subprocess so
      it returns things more easily
- [ ] make a sphinx site
  - [ ] convert readme to rst (change in pyproject.toml as well)
- [ ] push to conda (in addition to pypi)

# Notes For Grant

- `flit build --format wheel`
- `twine upload dist/*`
