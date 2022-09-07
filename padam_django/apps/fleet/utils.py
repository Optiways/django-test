

def update_fields_instance(instance, fields, save=False):
    [setattr(instance, key, val) for key, val in fields.items()]
    if save:
        instance.save()
