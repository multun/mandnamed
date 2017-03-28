import inspect
from functools import wraps

class Mandatory(object):
    pass

def mandatory_named(f):
    sig = inspect.getargspec(f)
    mandatory = [(a,v == Mandatory) for a,v in zip(reversed(sig.args), reversed(sig.defaults))]
    mandatory.reverse()
    fixed = len(sig.args) - len(sig.defaults)

    @wraps(f)
    def clos(*args, **kwargs):
        for a in mandatory[len(args) - fixed:]:
            if a[1] and not a[0] in kwargs:
                raise TypeError(f'Missing mandatory argument {a[0]} for function {f}')
        return f(*args, **kwargs)
    return clos
