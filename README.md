Hindent is a syntax wrapper around lisps.
It simply allows you to use hanging indents as
a way to nest parenthesis. For example:

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

Or another way to think about it is
to do the same thing, but simply insert
the parenthesis instead of collapsing. For example

```
+
  -
    4
    1
  2

; goes to

+
  (-
    4
    1)
  2

; which goes to

(+
  (-
    4
    1)
  2)

```

It's the same either way because the lisps
we're translating to don't mind whitespace.

# How it works

Hindent simply parses the Hindent code and
inserts parenthesis according to the specification.
And as a side feature, it also will let you run that
code in a lisp if you want to.

# Installation

1. `pip install hindent`
2. [Install clojure](https://clojure.org/guides/install_clojure#java)
   and make sure it's on your path by running `clojure -Sdescribe`.
   - This also works with other lisps or schemes. If
     you want to do that, the
     notes in the module dosctrings explain how to use a different lisp
3. The syntax highlighter for vs code is
   [`Hindent Lang`](https://marketplace.visualstudio.com/items?itemName=GrantSmith.hindent-lang).  You can find
   it in the normal extensions menu / marketplace.

# Usage

I think a nice way to interactively run programs is with jupyter.
So, I recommend opening up a jupyter notebook. Then, simply start to
import ``Hindent`` with `import Hindent as h`, and the docstrings/code-hover
will guide you from there.


# Parsing Spec

- the translater supports literate programming. It does so
  by putting block comments on equal footing with code. To
  toggle back and forth between code and block comment,
  put a lone period on a line.
  - For reasons of textmate grammars and syntax highlighting,
    we had to make the file start as code, rather than starting
    as block comment. We would have preferred it the other way,
    but we think it's okay.  We're thankful for how awesome vs
    code and textmate are.
- the parser/translater will put a new line after the source code
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
      is at 0, and it isn't already wrapped in parenthesis, then wrap the current line in parenthesis
    - if the current indentation level (and also the indentation level of the following line)
      is nonzero, then do nothing
- to allow the user to override the indenting and indent the code without
  hindent paying attention to the indent, you can put a `. ` before
  a line of code at the indent level you want that code to be treated as.
  There is an example in `example.hin`

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

- [ ] if a function doesn't have any argument, and
      we want to call it, we still need to wrap it in
      parens. see the `clojure-examples.hin` for an example
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
