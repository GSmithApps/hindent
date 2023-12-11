Hindent is a new programming language.
It's purpose is to use
whitespace and indentation to insert implied
parenthesis, which means you don't have to write
the parenthesis, which makes the code look cleaner.
That might not sound like much, but you might
be surprised at the difference it makes.

For example, here
is some Hindent code... it's nice and pretty

```
+ 2 2
```

And the corresponding lisp code is

```
(+ 2 2)
```

The Hindent interpreter executes
Hindent code by translating
it to lisp then executing it using
existing lisp interpreters/compilers.

More details are given in the
parsing section below, and more examples
are in `/examples/example.hin`.

# Installation

1. `pip install hindent`
2. [Install clojure](https://clojure.org/guides/install_clojure#java)
   (and Java) and make sure clojure is on your path by running `clojure -Sdescribe`.
   - This also works with lisps other than clojure. If
     you want to do that, the
     notes in the module dosctrings explain how to use a different lisp
3. The syntax highlighter for vs code is
   [`Hindent Lang`](https://marketplace.visualstudio.com/items?itemName=GrantSmith.hindent-lang).  You can find
   it in the normal extensions menu / marketplace.

# Usage

I think a nice way to interactively run programs is with jupyter.
So, I recommend opening up a jupyter notebook. Then, simply start to
import ``Hindent`` with `import hindent as h`, and the docstrings/code-hover
will guide you from there.


# Parsing Spec

Hindent is really just a syntax wrapper.
It simply allows you to use indents as
a way to nest parenthesis. 

It is extra handy with lisps because
they use a lot of parenthesis. So that's why
most of the examples are lisp.

Here is how it works

## Pre-Parse

- the translater supports literate programming. It does so
  by putting block comments on equal footing with code. To
  toggle back and forth between code and block comment,
  put a lone comma on a line.
  - For reasons of textmate grammars and syntax highlighting,
    we had to make the file start as code, rather than starting
    as block comment. We would have preferred it the other way,
    but we think it's okay.  We're thankful for how awesome vs
    code and textmate are.
- the parser/translater will put a new line after the source code
  to ensure the final dedent is correct
- lines that start with `;` are comments and will be ignored


## Main Parsing

- calculate the number of spaces each line starts with.
- Then divide by 2 to determine the indentation level
- then, for each line find the difference in indentation level
  between that line and the following line
  - if the indentation level goes up, then after the current line, add opening parenthesis
    according to the number of indents.
  - if the indentation level goes down, then after
    the current line, add closing parenthesis
    according to the number of dedents.
  - if the indentation level remains the same, do nothing
- The notes in this bullet are
  best illustrated with examples.  There
  are some good ones in `/examples/example.hin`.
  Anyway, here is an attempt at an explanation:
  to allow the user to pick an indentation level
  other than what the textual code would otherwise look like,
  the user can lead a line with `. `.  This forces
  Hindent to treat the line's indentation where the `.` is
  rather than where the rest of the code (or lack thereof) is.
  Again, please see the examples in `/examples/example.hin`.

# Miscellaneous Thoughts

This framework works for any language.  We just mostly
discuss lisps because it has the biggest impact and is
cleanest on lisps.

One heads up is that if you try to use it on languages that
are whitespace-sensitive (haskell, python, etc), it will probably
have trouble because it could theoretically change indentation
while inserting parenthesis or removing the hindent markup.

In general, I think translating into whitespace-sensitive
languages is probably harder than translating into whitespace-insensitive
languages.  But translating *from* whitespace-sensitive languages
(like Hindent) is totally okay.

# ToDo

- [ ] figure out how to process whitespace and
      empty lines in the new setup
      - [ ] rewrite all the example code.
- [ ] redo the example code for map
- [ ] change the verbage from `translate` to something else. I can't think
      of what. It's hard to say. really all it does is remove comments and whitespace
      then add parenthesis.
- [ ] maybe get it out of running as a subprocess so
      it returns things more easily
- [ ] make a sphinx site
  - [ ] convert readme to rst (change in pyproject.toml as well)
- [ ] push to conda (in addition to pypi)

# unsolved

I'm not sure if this syntax retains lisp's
homoiconicity. That's something to think more about

# clojure replacements

- list for lists
- vector for vectors
- hash-map for maps
- set or hash-set for sets

# Notes For Grant

- `flit build --format wheel`
- `twine upload dist/*`
