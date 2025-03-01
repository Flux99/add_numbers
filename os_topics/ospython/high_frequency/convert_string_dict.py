def convert_to_dict(string):
    keys = string.split('_')
    stack = []
    current_dict = {}
    for key in keys:
        if len(stack) == len(keys) - 1:
            stack[-1][prev_key] = key
        else:
            new_dict = {}
            current_dict[key] = new_dict
            stack.append(current_dict)
            current_dict = new_dict
            prev_key = key
    return stack[0]


string = 'gfg_is_best_for_geeks'
result = convert_to_dict(string)
print(string)
print(result)
