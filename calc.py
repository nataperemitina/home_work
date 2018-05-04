__all__ = [
    'convert',
    'calc',
]

def convert_to_list(expr):
    operation_lst = []
    new_expr = []
    
    def add_operations():
        nonlocal operation_lst
        nonlocal new_expr
        j = 0
        count = len(operation_lst)
        while j < count:
            operation = operation_lst.pop()
            if operation == '(':
                break
           
            new_expr.append(operation)
            j += 1

    def on_opening_brace(char):
        nonlocal operation_lst
        operation_lst.append(char)

    def on_closing_brace(char):
        add_operations()
       

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

        nonlocal operation_lst
        nonlocal new_expr
        j = 0
        count = len(operation_lst)
        while j < count:
            operation = operation_lst.pop()
           
            if priority_dict.get(operation) >= priority:
                new_expr.append(operation)
            else:
                operation_lst.append(operation)

            if operation == '(':
               break

            j += 1

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
    digit_accum = ''

    while i < expr_len:
        char = expr[i]
        if char.isdigit():
            digit_accum += char
        else:
            if digit_accum:
                new_expr.append(digit_accum)
                digit_accum = ''
            if not char.isspace():
                if char == '/' and i != expr_len -1 and expr[i + 1] == '/':
                    char += '/'
                    i += 1
                action = action_dict.get(char)
                if action:
                    action(char)
        i += 1

    if digit_accum:
        new_expr.append(digit_accum)

    add_operations()
    return new_expr

def convert(expr):    
    return ' '.join(convert_to_list(expr))
    
def add(i,j):
    return i + j

def subtract(i, j):
    return i - j

def multiply(i, j):
    return i * j

def divide(i, j):
    return i / j

def remainder(i, j):
    return i % j

def floored_quotient(i, j):
    return i // j

def to_power(i, j):
    return i**j

def calc(expr):
    operation_dict = {
        '+' : add,
        '-' : subtract,
        '*' : multiply,
        '/' : divide,
        '%' : remainder,
        '//' : floored_quotient,
        '^' : to_power,
    }
    expr_lst = convert_to_list(expr)
    stack = []
    for op in expr_lst:
        if op.isdigit():
            stack.append(int(op))
        else:
            operation = operation_dict.get(op)
            if operation:
                j = stack.pop() if len(stack) > 0 else 0
                i = stack.pop() if len(stack) > 0 else 0
                stack.append(operation(i, j))

    return stack.pop()

if __name__ == '__main__':
    expr = input()
    print(calc(expr))

