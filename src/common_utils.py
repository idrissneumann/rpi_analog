import os

def is_not_empty (var):
    if (isinstance(var, bool)):
        return var
    elif (isinstance(var, int)):
        return False
    empty_chars = ["", "null", "nil", "false", "none"]
    return var is not None and not any(c == var.lower() for c in empty_chars)

def get_env_var(key, default_value):
    value = default_value
    ukey = key.upper()
    if is_not_empty(os.environ.get(ukey)):
        value = os.environ[ukey]
    return value

def is_true (var):
    if (isinstance(var, bool)):
        return var
    true_chars = ["true", "enabled", "enable", "ok", "on", "yes"]
    return is_not_empty(var) and any(c == var.lower() for c in true_chars)

def is_false (var):
    return not is_true(var)

def is_empty (var):
    return not is_not_empty(var)

def is_empty_array(array):
    return array is None or len(array) <= 0 or not any(is_not_empty(elem) for elem in array)

def is_not_ok(body):
    return not "status" in body or body["status"] != "ok"

def is_empty_arg(args, key):
    return not key in args or is_empty_array(args[key])

def is_not_numeric(var):
    return not isinstance(var, int) and (is_empty(var) or not var.isnumeric())

def is_bad_number(var):
    return is_not_empty(var) and is_not_numeric(var)

def cast_boolean(var):
    if is_true(var):
        return True
    else:
        return False

def cast_int(var):
    if is_not_numeric(var):
        return None
    elif (isinstance(var, int)):
        return var
    else:
        return int(var)

def cast_array(var):
    if not isinstance(var, list) and is_not_empty(var):
        array = []
        array.append(var)
        return array
    elif isinstance(var, list) and not is_empty_array(var):
        return var
    return None

def get_env_var_array(key):
    value = get_env_var(key, None)
    if is_empty(value):
        return None

    array = value.split(",")
    if is_empty_array(array):
        return None

    return array
