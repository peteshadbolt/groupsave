"""
Define key formats 
"""

def fullname_key(crs):
    return "fullname:{:}".format(crs)


def journey_key(crs1, crs2, minute):
    return "journey:{:}:{:}:{:}".format(crs1, crs2, minute)


def platform_key(crs, minute):
    return "platform:{:}:{:}".format(crs, minute)

