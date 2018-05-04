__all__ = [
    'convert',
    'calc',
]

def convert(expr):
    operation_lst = []
    new_expr = []
    open_brace_i = []

    def on_opening_brace(char):
        nonlocal operation_lst
        nonlocal open_brace_i
        operation_lst.append(char)
        open_brace_i.append(len(operation_lst) - 1)

    def on_closing_brace(char):
        nonlocal open_brace_i
        last_open_brace_i = open_brace_i.pop() or 0
        nonlocal operation_lst
        nonlocal new_expr

        operation_lst.pop(last_open_brace_i)
        j = 0
        op_len = len(operation_lst) - last_open_brace_i
        while j < op_len:
            new_expr.append(operation_lst.pop())
            j += 1

#        new_expr.extend(operation_lst[last_open_brace_i+1::])
#        operation_lst = operation_lst[:last_open_brace_i:]

    priority_dict = {
        '+' : 1,
        '-' : 1,
        '*' : 2,
        '/' : 2,
        '%' : 2,
        '//' : 2,
        '^' : 3,
        '(' : 0,
        ')' : 0,
    }

    def on_operation(char):
        priority = priority_dict.get(char)
        if not priority:
            return

        nonlocal open_brace_i
        start_i = open_brace_i[len(open_brace_i)-1] if len(open_brace_i) else 0

        nonlocal operation_lst
        nonlocal new_expr

        while start_i < len(operation_lst):
            other_priority = priority_dict.get(operation_lst[start_i])
            if other_priority:
                if other_priority >= priority:
                    new_expr.append(operation_lst.pop(start_i))
            start_i += 1

        operation_lst.append(char)

    action_dict = {
        '+' : on_operation,
        '-' : on_operation,
        '*' : on_operation,
        '/' : on_operation,
        '%' : on_operation,
        '//' : on_operation,
        '^' : on_operation,
        '(' : on_opening_brace,
        ')' : on_closing_brace,
    }

    i = 0
    expr_len = len(expr)

    while i < expr_len:
        if expr[i].isdigit():
            new_expr.append(expr[i])
        elif not expr[i].isspace():
            action = action_dict.get(expr[i])
            if action:
                action(expr[i])

        i += 1

    j = 0
    op_len = len(operation_lst)
    while j < op_len:
        new_expr.append(operation_lst.pop())
        j += 1

    return ' '.join(new_expr)
    
def calc(expr):
    print(expr)

if __name__ == '__main__':
    expr = input('\nВведите выражение:')
    print(convert(expr))