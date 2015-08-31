"""
Define key formats 
"""

def timebin(when):
    return when.timestamp / 60

def fullname_key(crs):
    return "fullname:{:}".format(crs)


def platform_key(crs, when):
    return "platform:{:}:{:}".format(crs, timebin(when))


def journey_key(crs1, crs2, when):
    return "journey:{:}:{:}:{:}".format(crs1, crs2, timebin(when))

