=============
Miscellaneous
=============



Miscellaneous Thoughts
----------------------

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


Caveat
------

You can't write regular lisp code on indent 0
or at the beginning of a code block.
it will wrap in parenthesis


unsolved
--------

I'm not sure if this syntax retains lisp's
homoiconicity. That's something to think more about


clojure replacements
--------------------

- list for lists
- vector for vectors
- hash-map for maps
- set or hash-set for sets