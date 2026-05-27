class AffiliateNotFoundError(Exception):
    """Raised when an affiliate cannot be found in the system."""
    pass

class DuplicateDocumentError(Exception):
    """Raised when attempting to create an affiliate with an already existing document number."""
    pass

class InvalidContributionAmountError(Exception):
    """Raised when a contribution amount is invalid (e.g., negative or zero)."""
    pass
