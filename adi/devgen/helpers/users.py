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

def userExists(context, user_id):
    return context.portal_membership.getMemberById(user_id) is not None
