===========
Explanation
===========

Hindent is really just string processor that
inserts parenthesis based on indentation. 

And just
for convenience, we also put in a way to execute code.
That code execution part might feel like a core
part of Hindent, but it isn't. The real important parts
are the syntax and how Hindent reads it to insert
parenthesis.

This method for implying parenthesis with whitespace
happens to be extra handy with lisps because
they use a lot of parenthesis, and no commas to
separate things (just spaces). So that's why
most of the examples are lisp.

Here is how it works

Pre-Parse
---------

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
- lines that start with ``;`` are comments and will be ignored


Main Parsing
------------

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
  are some good ones in the examples page.
  Anyway, here is an attempt at an explanation:
  to allow the user to pick an indentation level
  other than what the textual code would otherwise look like,
  the user can lead a line with ``.``.  This forces
  Hindent to treat the line's indentation where the ``.`` is
  rather than where the rest of the code (or lack thereof) is.
  Again, please see the examples page.

