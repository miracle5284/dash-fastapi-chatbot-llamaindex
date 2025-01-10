def extract_from_dict(dict_obj, *keys):
    return [dict_obj.get(key) for key in keys]