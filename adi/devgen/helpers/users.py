from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

def addUser(context, user_email):
    """
    Use prefix of email as user_id, user_name and passwd.
    If user exists, fail silently.
    """
    user_id = user_email.split('@')[0]
    if not userExists(context, user_id):
        passwd = user_id
        properties = {
            'username': user_id,
            'fullname': user_id.encode("utf-8"),
            'email': user_email
            }
        pt = context.portal_registration
        pt.addMember(user_id, passwd, properties=properties)

def getCurrentUser(context):
    return context.request.AUTHENTICATED_USER.getUserName()

def getUser(context, user_id):
    """
    Get user-obj by user-id, requires holding the Manager-role.
    """
    if isView(context): context = context.aq_parent
    return context.portal_membership.getMemberById(user_id)

def isView(context):
    return isinstance(context, BrowserView)

def isLoggedIn(context):
    return getCurrentUserId(context) != 'Anonymous user'

def setUserFullname(context, user, user_fullname):
    """
    Set a user's fullname.
    """
    user.fullname = user_fullname
    if user.getProperty('fullname') != user_fullname:
        user.setMemberProperties(mapping={"fullname":user_fullname})

def userExists(context, user_id):
    return getUser(context, user_id) is not None

