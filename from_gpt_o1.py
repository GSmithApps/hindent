import re
from pretty_print_s_exp import pretty_s_expr

CORNER_OPEN  = '┌'
CORNER_SPLIT = '├'
CORNER_CLOSE = '└'

def parse_box_drawing(lines):
    """
    Parse a list of lines that use box-drawing characters to represent
    Lisp-like structure. Return a nested Python list that models an S-expression.
    """
    # The stack of nested lists:
    # Each element is the *list* we’re currently adding tokens/sub-lists to.
    stack = [[]]  # Start with a root list

    def current_list():
        return stack[-1]

    for line in lines:
        # Strip trailing spaces/newlines
        line = line.rstrip('\n')
        
        # We'll extract tokens (the part that isn’t box art).
        # We'll also look for corners (┌, ├, └).
        
        # 1) Separate out the box-drawing prefix from the actual token text.
        #    We'll do a quick match on box-drawing chars and maybe spaces.
        match = re.match(r'^([\u2500-\u257F\s]+)(.*)$', line)
        if match:
            box_part = match.group(1)
            token_part = match.group(2).strip()
        else:
            # No match means maybe empty line or no box chars
            box_part = ""
            token_part = line.strip()
        
        # 2) Figure out which corners appear in `box_part`.
        #    e.g. if we see "│ ┌────", corners = ['┌']
        #         if we see "└─┴─┴─┴─┴", corners might be ['└', '┴', '┴', '┴', '┴'] 
        #         but to keep it simple, we'll focus on the big three: ┌, ├, └
        corners = re.findall(r'[┌├└]', box_part)
        
        # 3) Process each corner in the order they appear from left to right.
        for corner in corners:
            if corner == CORNER_OPEN:
                # ┌ means "open a new child list"
                new_list = []
                current_list().append(new_list)
                stack.append(new_list)
            
            elif corner == CORNER_SPLIT:
                # ├ means "close the current child list, open a sibling list at same level"
                # So we pop once, then create a new sibling list
                if len(stack) > 1:
                    stack.pop()
                new_list = []
                current_list().append(new_list)
                stack.append(new_list)
            
            elif corner == CORNER_CLOSE:
                # └ means "close one or more lists"
                # Usually a line with a single └ means close one level,
                # but if you see multiple corners in the same line, you might close more.
                if len(stack) > 1:
                    stack.pop()
                # If you had multiple `└` in the same line, we’d pop multiple times,
                # but that often appears as └─┴ etc. If you want that:
                #   while corner == CORNER_CLOSE and len(stack) > 1:
                #       stack.pop()
                # But let's keep it simpler for now.
        
        # 4) Now add any tokens to the *current* top list.
        if token_part:
            tokens = token_part.split()
            current_list().extend(tokens)

    # Finally, if the box drawing didn’t close everything, we might still have leftover frames
    # Usually you'd want to close them, so let's pop until we reach the root:
    while len(stack) > 1:
        stack.pop()
    
    return stack[0]


def to_s_expr(ast):
    """
    Convert a nested Python list (like ['define', [...], [...]] ) 
    into a Lisp S-expression string.
    """
    if isinstance(ast, list):
        return "(" + " ".join(to_s_expr(item) for item in ast) + ")"
    else:
        return str(ast)


if __name__ == "__main__":
    sample_code = [
        "┌────",
        "│ define",
        "│ ┌────",
        "│ │ counter-first start-num",
        "│ ├────",
        "│ │ lambda",
        "│ │ ┌────",
        "│ │ │ ",  # empty payload
        "│ │ ├────",
        "│ │ │ cons",
        "│ │ │ start-num",
        "│ │ │ ┌────",
        "│ │ │ │ counter-first",
        "│ │ │ │ ┌────",
        "│ │ │ │ │ + start-num 1",
        "└─┴─┴─┴─┴────"
    ]
    
    parsed = parse_box_drawing(sample_code)
    print("PARSED STRUCTURE:")
    print(pretty_s_expr(parsed))
    print("\nAS S-EXPR:")
    print(to_s_expr(parsed))
