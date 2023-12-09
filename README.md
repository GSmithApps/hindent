I want to make a programming language like the following, in which we will use hanging indents to determine nesting and parenthesis, and then insert the parenthesis, then evaluate the code (with parenthesis inserted) in scheme

```
+
  2
  2

```

- The first thing is to read the file and calculate
  the number of spaces each line starts with.
- Then divide by 2 to determine the indentation level
- the first line should have no indents
- the last line should be blank
- any amount of whitespace that contributes to a blank line
  (other than the last line) should be replaced with a single
  new line character. For example, `\n\n\n` should be replaced
  with `\n`, and `\n   \n` should also be replaced with `\n`
- then, for each line find the difference in indentation level
  between that line and the following line
  - if the indentation level goes up one, then add an opening parenthesis before the line
  - if the indentation level goes down, then add a closing parenthesis after the line
    according to the number of dedents.
  - if the indentation level remains the same, then we have to check one more thing:
    - if the current indentation level (and also the indentation level of the following line)
      is at 0, then wrap the current line in parenthesis
    - if the current indentation level (and also the indentation level of the following line)
      is nonzero, then do nothing
- can we write a function that does this, and returns
  the string with those parenthesis inserted?