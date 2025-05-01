"""Utility functions for settings modules."""

def deep_update(d, u):
    """Recursively update nested dictionaries.
    
    Args:
        d: The dictionary to update
        u: The dictionary with updates
        
    Returns:
        The updated dictionary
    """
    for k, v in u.items():
        if isinstance(v, dict):
            d[k] = deep_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d