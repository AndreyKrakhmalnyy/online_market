from collections.abc import Iterable

def recursive_sum(*args, dephts: list[int] = None) -> int | float:
    if dephts is None:
        dephts = []
    
    sum = 0
    errors = []
    
    for index, arg in enumerate(args):
        if isinstance(arg, Iterable) and not isinstance(arg, str):
            new_sum, new_errors = recursive_sum(*arg, dephts=[*dephts, index])
            
            if len(errors) > 0:
                errors.extend(new_errors)
            else:
                sum += new_sum
                
        elif isinstance(arg, int) or isinstance(arg, float):    
            sum += arg
        else:
            errors.append([*dephts, index])

    if len(dephts) == 0:
        print(errors)
        
    return sum, errors


print(recursive_sum(1, (3,4,6), 'qwe', 2, [5,6], 'abc'))