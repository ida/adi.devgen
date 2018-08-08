from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.globalrequest import getRequest
from zope.site.hooks import getSite

from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletRetriever


def getMappingForContextOfManager(context, manager):
    mapping = getMultiAdapter((context, manager), IPortletAssignmentMapping)
    return mapping

def getRetrieverForContextOfManager(context, manager):
    retriever = getMultiAdapter((context, manager,), IPortletRetriever)
    return retriever

def getPortletById(id_, assignment, retriever):
    portlet = None
    for assignment in retriever.getPortlets():
        if assignment["name"] == id_:
            portlet = assignment["assignment"]
    return portlet

def getRenderer(context, request, view, manager, assignment):
    renderer = getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)
    renderer = renderer.__of__(context)
    return renderer

def getPortletIds():
    """
    page = context['page']
    for d in dir(page):
        if d.find('get') > -1:
            pass#rint d
    tal = page.getRawText()
    """
    tal = u"<b tal:content='context/Title'/>"
    ids = []


    request = getRequest()
    context = getSite()

    manager_name = "plone.leftcolumn"
    manager = getUtility(IPortletManager, name=manager_name, context=context)

    mapping = getMappingForContextOfManager(context, manager)
    retriever = getRetrieverForContextOfManager(context, manager)

    view = context.restrictedTraverse('@@plone')

    renderer = getRenderer(context, request, view, manager, assignment)

    for id, assignment in mapping.items():
        portlet = getPortletById(id, assignment, retriever)
        portlet.tal = tal
        renderer.update()
        html = renderer.render()
        ids.append(id)

    return ids


