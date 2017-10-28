from zope.globalrequest import getRequest

def getContextOfRequest(request):
    published = request.get('PUBLISHED', None)
    context = getattr(published, '__parent__', None)
    if context is None:
        context = request.PARENTS[0]
    return context

def getRequest():
    return getRequest()

def getRequestOfEvent(event):
    return event.object.REQUEST
