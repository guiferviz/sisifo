def validate_entity_in_out(entity=None, entity_in=None, entity_out=None):
    entity_in = entity_in or entity
    entity_out = entity_out or entity_in

    if not entity_in:
        raise ValueError("Input entity must have a valid value")

    return entity_in, entity_out


def validate_column_in_out(column=None, column_in=None, column_out=None):
    column_in = column_in or column
    column_out = column_out or column_in

    if not column_in:
        raise ValueError("Input column must have a valid value")

    return column_in, column_out
