def slugify(str):
    """Turn a string into a URL slug"""
    return str.lower().replace(' ', '-') \
            .replace('.','').replace('/', '')
