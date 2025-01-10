def return_or_throw(to_return, message=None, exception_class=None):
    if not to_return:
        raise exception_class or Exception(message)
    return to_return


def extract_attrs(obj, *attrs):
    return [getattr(obj, attr) for attr in attrs]
