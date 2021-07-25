def validate_column_out(column=None, column_out=None):
    column_out = column_out or column

    if not column_out:
        raise ValueError("Output column must have a valid value")

    return column_out


def validate_column_in_out(column=None, column_in=None, column_out=None):
    column_in = column_in or column
    column_out = column_out or column_in

    if not column_in:
        raise ValueError("Input column must have a valid value")
    if not column_out:
        raise ValueError("Output column must have a valid value")

    return column_in, column_out


def validate_entity_out(entity=None, entity_out=None):
    entity_out = entity_out or entity

    if not entity_out:
        raise ValueError("Output entity must have a valid value")

    return entity_out


def validate_entity_in(entity=None, entity_in=None):
    entity_in = entity_in or entity

    if not entity_in:
        raise ValueError("Input entity must have a valid value")

    return entity_in


def validate_entity_in_out(entity=None, entity_in=None, entity_out=None):
    entity_in = entity_in or entity
    entity_out = entity_out or entity_in

    if not entity_in:
        raise ValueError("Input entity must have a valid value")
    if not entity_out:
        raise ValueError("Output entity must have a valid value")

    return entity_in, entity_out


def validate_list_of_columns(columns):
    if columns is None or type(columns) != list or len(columns) == 0:
        raise ValueError("Columns should be a non-empty list")

    return columns
