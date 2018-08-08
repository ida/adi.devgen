from plone.stringinterp.browser import SubstitutionInfo

def getSubstitutables(context, request):
    """Call this from within a BrowserView."""
    substitutable_ids = []
    substitution_info = SubstitutionInfo(context, request)
    substitution_list = substitution_info.substitutionList()
    for category in substitution_list:
        substitutables =  category['items']
        for substitutable in substitutables:
            for substituti in substitutable:
                if substituti == 'id':
                    substitutable_ids.append(substitutable[substituti])
    return substitutable_ids

