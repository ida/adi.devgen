def hasState(obj):
    return hasWorkflow(obj)

def hasWorkflow(obj):
    wf = obj.portal_workflow
    if len( wf.getWorkflowsFor(obj) ) > 0: return True
    else: return False

def getState(obj):
    return obj.portal_workflow.getInfoFor(obj, 'review_state')

