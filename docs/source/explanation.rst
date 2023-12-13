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

Example
-------

Hindent counts the indentations,
and inserts parenthesis according
to the indentation level.

In a little
more detail, it does the following.
And as you're reading, have in your head that it
always marches forward and pays attention
to the current line and the following line.
And depending on their indentation, it may
or may not insert parenthesis at the end of the current
line.

Here is the original hindent code:

.. code-block::

   println
     + 1 2

1. Start with the line before ``println``.  Assuming
   it is blank, and ``println`` isn't, it assumes a block
   of code is starting, and inserts an opening parenthesis at the end
   of the current line.

.. code-block::

   (
   println
     + 1 2

2. Moves to the next line, (``println``), and the
   following line, (``+ 1 2``).  Because the indentation
   of the following line is greater than the current line,
   it inserts an opening parenthesis at the end of the current line.

.. code-block::

   (
   println (
     + 1 2

3. Moves to the next line, (``+ 1 2``), and the
   following line, which is blank.  Because the indentation
   of the following line is less than the current line,
   it inserts a closing parenthesis at the end of the current line.
   Additionally, because the next line is blank, it assumes
   the block of code is ending, and inserts a closing parenthesis.

.. code-block::

   (
   println (
     + 1 2 ))

4. Done

In this way, we can write lisp programs 
that can be easier to read.