from zope.globalrequest import getRequest

def getRequest():
    return getRequest()

def getRequestOfEvent(event):
    return event.object.REQUEST
