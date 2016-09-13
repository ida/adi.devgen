def getState(obj):
    """
    Return workflow-state-id or None, if no workflow is assigned.
    Show possible error on the console and log it.
    """
    if hasWorkflow(obj):
        try: return obj.portal_workflow.getInfoFor(obj, 'review_state')
        except ExceptionError as err: obj.plone_log(err)
    else: return None

def getTransitions(obj):
    """
    Return the identifiers of the available transitions as a list.
    """
    transitions = []
    trans_dicts = obj.portal_workflow.getTransitionsFor(obj)
    for trans_dict in trans_dicts:
        transitions.append(trans_dict['id'])
    return transitions

def hasWorkflow(obj):
    """
    Return boolean, indicating whether obj has a workflow assigned, or not.
    """
    return len(obj.portal_workflow.getWorkflowsFor(obj)) > 0

def hasTransition(obj, transition):
    if transition in getTransitions(obj): return True
    else: return False

def isSite(obj):
    return len(obj.getPhysicalPath()) == 2

def publishReferences(obj, eve, RUHTLESS=False):
    """
    If an obj gets published, publish its references, too.
    If an item doesn't have a workflow assigned and RUHTLESS
    is passed to be True, publish next upper parent with a workflow.
    """
    states = PublicRank.states
    state = getState(obj)
    transition = eve.action

    if state in states:
        refs = obj.getRefs()
        for ref in refs:
            ref_state = getState(ref)
            if ref_state:
                if isMorePublic(state, ref_state):
                    setState(ref, transition)
            else: # no workflow assigned
                if RUTHLESS:
                    setStateRelentlessly(ref, transition)

def setState(obj, transition):
    """
    Execute transition, return possible error as an UI-message,
    instead of consuming the whole content-area with a raised Exeption.
    """
    path = '/'.join(obj.getPhysicalPath())
    messages = IStatusMessage(getRequest())
    if hasWorkflow(obj):
        if hasTransition(obj, transition):
            try:
                obj.portal_workflow.doActionFor(obj, transition)
            except Exception as error:
                messages.add(error, type=u'error')
        else:
            message = 'The transition "%s" is not available for "%s".'\
                       % (transition, path)
            messages.add(message, type=u'warning')
    else:
        message = 'No workflow retrievable for "%s".' % path
        messages.add(message, type=u'warning')

def setStateRelentlessly(obj, transition):
    """
    If obj has no workflow, change state of next
    upper parent which has a workflow, instead.
    """
    while not getState(obj, state):
        obj = obj.getParentNode()
        if isSite(obj): break
    setState(obj, transition)

def warnAboutPossiblyInaccessibleBackReferences(obj, eve):
    """
    If an obj is about to switch to a lesser public state than it
    has and is referenced of other item(s), show a warning message
    with the URL(s) of the referencing item(s), so the user can check,
    if the link is still accessible for the intended audience.
    """
    states = PublicRank.states
    item_path = '/'.join(obj.getPhysicalPath())[2:]
    target_state = str(eve.new_state).split(' ')[-1][:-1]
    refs = obj.getBackReferences()

    for ref in refs:
        ref_state = getState(ref)
        if isMorePublic(ref_state, target_state):
            ref_path = '/'.join(ref.getPhysicalPath())[2:]
            messages = IStatusMessage(getRequest())
            message = u'This item "%s" is now in a less published state than \
            item "%s" of which it is referenced by. You might want to check, \
            if this item can still be accessed by the intended audience.' \
            % (item_path, ref_path)
            messages.add(message, type=u'warning')

