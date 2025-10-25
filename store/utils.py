
def get_attr(obj, attr, default=None):
    """
    Safely get attribute from either a dict or a model object.
    
    Args:
        obj: Either a dict or a Django model instance
        attr: The attribute/key name to retrieve
        default: Default value if attribute not found
    
    Returns:
        The value of the attribute or default
    """
    if isinstance(obj, dict):
        return obj.get(attr, default)
    else:
        return getattr(obj, attr, default)


def get_model_name(obj):
    """Get the name attribute from either a dict or model object."""
    return get_attr(obj, 'name', 'Unknown')


def get_model_slug(obj):
    """Get the slug attribute from either a dict or model object."""
    return get_attr(obj, 'slug', '')


def get_model_id(obj):
    """Get the id attribute from either a dict or model object."""
    return get_attr(obj, 'id', None)


def get_model_price(obj):
    """Get the price attribute from either a dict or model object."""
    return get_attr(obj, 'price', 0)


def get_model_stock(obj):
    """Get the stock attribute from either a dict or model object."""
    return get_attr(obj, 'stock', 0)


def get_category_slug(product_obj):
    """
    Get the category slug from a product, handling both dict and model objects.
    
    Args:
        product_obj: Either a dict (from ERPNext) or a Django Product model
    
    Returns:
        The category slug as a string
    """
    if isinstance(product_obj, dict):
        # For ERPNext data, category is already a string
        category = product_obj.get('category', '')
        # Convert to slug format
        return category.lower().replace(' ', '-') if category else ''
    else:
        # For Django models, get the category slug
        if hasattr(product_obj, 'category') and product_obj.category:
            return product_obj.category.slug
        return ''
