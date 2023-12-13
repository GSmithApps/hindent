.. Hindent documentation master file, created by
   sphinx-quickstart on Mon Dec 11 22:16:17 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Hindent's documentation!
===================================

Hindent is an alternate syntax for lisp code.  For example,
instead of writing

.. code-block::

   (println (+ 1 2))

You could write

.. code-block::

   println
     + 1 2

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

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   installation-and-usage
   explanation
   examples
   main
   execution
   misc

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

