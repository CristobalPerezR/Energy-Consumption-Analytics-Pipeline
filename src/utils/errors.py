class ValidationError(Exception):
    """Error when validating the dataframe against the schema."""
    pass

class InsertionError(Exception):
    """Error when inserting the dataframe into the database."""
    pass