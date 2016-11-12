from AccessControl.SecurityManagement import newSecurityManager
from plone.app.layout.viewlets.content import ContentHistoryViewlet
from plone.app.layout.viewlets.content import WorkflowHistoryViewlet
from zope.publisher.browser import TestRequest
from zope.site.hooks import getSite as portal


def getFullHistory(item):
    """
    http://docs.plone.org/develop/plone/content/history.html
    """
    history = None
    # TODO: user must exist in plonsite ! Zopeadmin can watch anyway.
    #admin = portal().acl_users.getUser('siteadmin')
    #newSecurityManager(request, admin)
    request = TestRequest()
    chv = ContentHistoryViewlet(item, request, None, None)
    # These attributes are needed, the fullHistory() call fails otherwise
    chv.navigation_root_url = chv.site_url = 'http://www.example.org'
    history = chv.fullHistory()
    return history

def getWorkflowHistory(item):
    """
    In contrary to 'context.workflowHistory()', of
    plone.app.viewlets, we can get the wf-history not
    only of the given context, but of any passed obj,
    by passing a fake REQUEST-var and overcome
    permission-restrictions, see:
    http://docs.plone.org/develop/plone/content/history.html
    """
    workflow_history = None
    request = TestRequest()
    # TODO: user must exist in plonsite ! Zopeadmin can watch anyway.
    #admin = portal().acl_users.getUser('siteadmin')
    #newSecurityManager(request, admin)
    chv = WorkflowHistoryViewlet(item, request, None, None)
    # These attributes are needed, the fullHistory() call fails otherwise
    chv.navigation_root_url = chv.site_url = 'http://www.example.org'
    workflow_history = chv.workflowHistory()
    return workflow_history

