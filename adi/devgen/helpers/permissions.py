def setLocalRole(context, user_id, role_id):
    # TODO: Check if role-id exists! Currently fails silently.
    context.manage_setLocalRoles(userid, [role_id])

def execute_under_special_role(portal, role, function, *args, **kwargs):
    """ Blatantly copied for reference, of:
    http://pydoc.net/Python/Products.EasyNewsletter/2.6.15/Products.EasyNewsletter.content.EasyNewsletter/ #noqa
    Execute code under special role priviledges.
    Example how to call::
        execute_under_special_role(portal, "Manager",
            doSomeNormallyNotAllowedStuff,
            source_folder, target_folder)

    @param portal: Reference to ISiteRoot obj whose access ctls we are using
    @param function: Method to be called with special priviledges
    @param role: User role we are using for the security context when calling \
                 the priviledged code. For example, use "Manager".
    @param args: Passed to the function
    @param kwargs: Passed to the function
    """

    sm = getSecurityManager()
    try:
        try:
            # Clone the current access control user and assign a new role
            # for him/her. Note that the username (getId()) is left in
            # exception tracebacks in error_log
            # so it is important thing to store
            tmp_user = UnrestrictedUser(
                sm.getUser().getId(), '', [role], '')

            # Act as user of the portal
            tmp_user = tmp_user.__of__(portal.acl_users)
            newSecurityManager(None, tmp_user)

            # Call the function
            return function(*args, **kwargs)

        except:
            # If special exception handlers are needed, run them here
            raise
    finally:
        # Restore the old security manager
        setSecurityManager(sm)

