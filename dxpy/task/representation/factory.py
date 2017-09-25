from .templates import template_class


def create_by_cls(template_class, *args, **kwargs):
    return template_class(*args, **kwargs)


def create_by_name(template_name, *args, **kwargs):
    return create_by_cls(template_class(template_name), *args, **kwargs)


def create(template_class_or_name, *args, **kwargs):
    if isinstance(template_class_or_name, str):
        return create_by_name(template_class_or_name, *args, **kwargs)
    else:
        return create_by_cls(template_class_or_name, *args, **kwargs)
