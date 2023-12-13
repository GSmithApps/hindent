======================
Installation and Usage
======================

Installation
------------

1. ``pip install hindent``
2. The syntax highlighter for vs code is
   `Hindent Lang <https://marketplace.visualstudio.com/items?itemName=GrantSmith.hindent-lang>`_.  You can find
   it in the normal extensions menu / marketplace.

If you want to also execute code,
(which you probably do), then you need
to have that language on your path.
You'd also need to configure your
executor, which is explained in the
page on execution.  The default
execution is Clojure, so if you
want to use the default, then
`install clojure <https://clojure.org/guides/install_clojure>`_
(and Java)

Usage
-----

I think a nice way to interactively run programs is with jupyter.
So, I recommend opening up a jupyter notebook. Then, simply start to
import ``Hindent`` with ``import hindent as h``, and the docstrings/code-hover
will guide you from there.
