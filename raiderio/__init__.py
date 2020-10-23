from raiderio.client_factory import CharactersList 


AVAIL_RESOURCES = ["character"]

class UnknownResource(Exception):
    pass

def resource(rtype):
    """Resource factory method."""
    if rtype == "characters":
        resource = CharactersList()
    else:
        raise UnknownResource('{0} not found. Please select from {1}'.format(rtype,
                              AVAIL_RESOURCES))
    return resource