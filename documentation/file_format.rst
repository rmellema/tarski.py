Tarski's World File Format
==========================
`tarski.py` is meant to work with `.wld` files from `Tarski's world`_. This file
format is however not defined, so it is written down here for future reference.
All information presented here has been collected by trial and error and looking
at the raw representation of these files, and are not endorsed by the authors
of the original software.

The format consists of three parts, a header, a body, and a footer, all of which
are seperated over one or multiple 'lines', which are seperated by carriage
returns.

Header
------
The header of a Tarski's World file seems to consist of debug information.
None of the presented information is necessary for the creation of the blocks
world. We will now present this information line by line.

1. The Version number of the producing Tarski's World.
2. The OS on which the producing Tarski's World was ran.
3. The letters 'Wld' followed by a letter. Purpose unknown, but might be for
   versioning reasons.
4. A line with large numbers seperated by letters. Purpose unknown. Seems to
   only be present from Tarski's world version 7.
5. A line with 's=' followed by a number. Purpose unknown, but seems to be the
   CPU time at the start of saving. Also only present from Version 7 onward.

Body
----
The body seems to be the same between version 6 and 7. It starts of with just
one number on a line, which specifies the number of blocks that are in this
file. Then, for each of these blocks it lists the following information, per
line:

1. The shape and the Size: `n m`
2. The location: `x y`
3. The name: `'i`

Where `x` is the x location, `y` is the y location, `i` is a letter that is the
name. Both `n` and `m` are numbers that range from 1 to 3, and whose meaning is
explained in the table below.

======= ============ =======
`n`/`m` Shape        Size
======= ============ =======
1       Tetrahedron  Small
2       Cube         Medium
3       Dodecahedron Large
======= ============ =======

Footer
------
The footer is a single line which starts with `s=` follewed by something that
looks like the CPU time. The whole file is ended by a single `;`.

.. _Tarski's World: https://ggweb.gradegrinder.net/tarskisworld
