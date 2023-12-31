========
Examples
========

Here are some examples of Hindent code

.. code-block::

   println "# Basic Math"
   
   println "2 + 2 = "
   
   println
     + 2 2


And some other examples would be:

.. code-block::

   println "(2 + 2) + 2 = "
   
   println
     +
       + 2 2
     2
   
   println "(2 ^ (2 + 2)) + 2 = "


Because Hindent simply adds parenthesis and does
nothing else, you can actually write lisp code
in Hindent and it will work just fine. The one caveat
is that you can't use any newlines or indentation
in your lisp code, because hindent will think it is meaningful.

For example

.. code-block::

   println "\n# Lisp code in Hindent"
   
   println (+ 2 2)
   
   println
     +
       Math/pow
       2
         + 2 2
     2



And we can define variables with:


.. code-block::

   println "\n# Variables"
   
   def x 4
   
   println
     + 2 x


And Functions with:

.. code-block::

   println "\n# Functions"
   
   println "The square of 2 is: "
   
   defn
   square
   [x]
     * x x
   
   ; and function calls are
   println
     square 2



And we can handle lists with:

.. code-block::

   println "\n# Lists"
   
   println
     list 1 2 3 4



and conditionals:

.. code-block::

   ; lisp conditional
   ; (if (> x 0)
   ;     (print "Positive")
   ;     (print "Non-Positive"))
   
   println "\n# Conditional"
   
   println
     if
       > 2 0
     "Positive"
     "Non-Positive"


and multiline strings:

.. code-block::

   println "\n# String appending"
   
   println
     str
     "This is the first line.\n"
     "And this is the second."


and a recursion example

.. code-block::

   ; (defun (factorial n)
   ;   (if (= n 0)
   ;       1
   ;       (* n (factorial (- n 1)))))
   
   println  "\n# Factorial"
   
   defn
   factorial
   [n]
     if
       = n 0
     1
       * n
         factorial
           - n 1
   
   println "Factorial of 4: "
   
   println
     factorial 4


overriding the indent

You can override the indent and make hindent
think the indentation is somewhere other than where
it would be by putting a dot character where you
want the indent to behave


.. code-block::

   println "\n# Overriding the indent with `.`"
   
   println
     +
     .  3
     . 4
     .     5
     .   5
     .         6 
   
   println
     +
       + 2 2
     .
       + 2 3



The only data structure remaining is the
hash table.  As you can see, the indent
override is helpful here

.. code-block::

   println "\n# Hash Tables"
   
   def my-map {:a 1, :b 2, :c 3}
   
   ; Using the map as a function
   println (my-map :a)  ; => 1
   
   def
   my-map-g
   {
   . :a 1,
   . :b 2,
   . :c 3
   }
   
   ; Using the map as a function
   println (my-map :b)  ; => 1

