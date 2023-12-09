I want to make a programming language like the following, in which we will use hanging indents to determine nesting and parenthesis, and then insert the parenthesis, then evaluate the code (with parenthesis inserted) in a lisp

```
+
  2
  2

```

- The first thing is to read the file and calculate
  the number of spaces each line starts with.
- Then divide by 2 to determine the indentation level
- the first line should have no indents
- the last line should be empty
- then, find the difference between each line's indentation level
  - so, in the example above, that would be 1, 0, -1
- Then, take all the positive numbers, and put that many opening
  parenthesis before that line
- then take all the negative numbers, and put that many
  closing parenthesis after that line.
- can we write a function that does this, and returns
  the string with those parenthesis inserted?