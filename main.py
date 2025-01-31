from from_gpt_o1 import parse_box_drawing_chunk

from pretty_print_s_exp import pretty_s_expr

def print_parsed_forms(forms):
    """
    Print each top-level form on its own, no extra parentheses wrapping them all.
    """
    for i, form in enumerate(forms):
        print(pretty_s_expr(form))
        print()  # blank line after each top-level form

# Example usage:
box_text = """
┌────
│ define
│ ┌────
│ │ counter-first start-num
│ ├────
│ │ lambda
│ │ ┌────
│ │ │ 
│ │ ├────
│ │ │ cons
│ │ │ start-num
│ │ │ ┌────
│ │ │ │ counter-first
│ │ │ │ ┌────
│ │ │ │ │ + start-num 1
└─┴─┴─┴─┴────

┌────
│ define
│ ┌────
│ │ counter-second start-num
│ ├────
│ │ lambda
│ │ ┌────
│ │ │ 
│ │ ├────
│ │ │ cons
│ │ │ start-num
│ │ │ ┌────
│ │ │ │ counter-first
│ │ │ │ ┌────
│ │ │ │ │ + start-num 1
└─┴─┴─┴─┴────
"""

forms = parse_box_drawing_chunk(box_text)
# forms should be a list of two items
print_parsed_forms(forms)

# This worked and printed the following:
# (
#   define
#   (
#     counter-first start-num)
#   (
#     lambda
#     ()
#     (
#       cons
#       start-num
#       (
#         counter-first
#         (
#           +
#           start-num 1)))))
# 
# (
#   define
#   (
#     counter-second start-num)
#   (
#     lambda
#     ()
#     (
#       cons
#       start-num
#       (
#         counter-first
#         (
#           +
#           start-num 1)))))

