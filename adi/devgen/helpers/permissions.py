def setLocalRole(context, user_id, role_id):
    # TODO: Check if role-id exists! Currently fails silently.
    context.manage_setLocalRoles(userid, [role_id])

