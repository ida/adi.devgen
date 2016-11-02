# 'Old-style'-collections are of content-type 'Topic' and
#  described in 'Products/ATContentTypes/tests/test_topictool.py'.
# 'New-style'-collections are of content-type 'Collection' and
#  described in 'plone/app/collection/tests/test_collection.py'.

from Acquisition import aq_parent


def addTopic(context):
    """Example for adding a "new-style"-collection."""
    collection = _createObjectByType("Collection", context, 'overdue',
        title='Overdue contexts',
        description='Steps where the expiration-date has passed by.')
    query = [{'i': 'portal_type',
              'o': 'plone.app.querystring.operation.selection.is',
              'v': ['Stepbycontext']},
             {'i': 'expires',
              'o': 'plone.app.querystring.operation.date.beforeToday',
              'v': ''}]
    collection.setQuery(query)
    collection.reindexObject() # update catalog

def addLastModifiedCollection(context):
    # Create collection:
    collection = _createObjectByType("Topic", context, 'latest-modified',
        title='Latest modified items',
        description='An overview of all items, sorted by latest modification.')

    # Set collection-criterion 'portal-type' to be 'Document':
    criterion = collection.addCriterion('Type', 'ATPortalTypeCriterion')
    criterion.setValue('Document')

    # Set collection-criterion 'relative-path' to be parent,
    # include grand-children and exclude parent in results:
    # criterion = collection.addCriterion('path', 'ATRelativePathCriterion')
    # criterion.setRelativePath('..')
    # criterion.setRecurse(True)

    # Set collection-criterion 'UID-path' to be parent,
    # include grand-children and parent in results:
    criterion = collection.addCriterion('path', 'ATPathCriterion')
    criterion.setValue([collection.aq_parent.UID()])
    criterion.setRecurse(True) # include grand-children

    # Sort results by latest modified item first:
    collection.setSortCriterion('modified', 'descending')
    # Update catalog:
    collection.reindexObject()

def addLastExpiredCollection(context):
    # Create collection:
    collection = _createObjectByType("Topic", context, 'overdue',
        title='Overdue contexts',
        description='Steps where the expiration-date has passed by.')

    # SORTING
    # Sort results by latest expired item first:
    collection.setSortCriterion('expires', 'descending')

    # VIEW
    # Enable and thereby also set the table-view as default-template:
    collection.setCustomView(True)
    # Set which columns shall show up in table-view:
    collection.setCustomViewFields(['Title', 'ExpirationDate'])

    # CRITERIA
    # Expiration date passed by:
    criterion = collection.addCriterion('expires', 'ATFriendlyDateCriteria')
    criterion.setValue(0) # now
    criterion.setOperation('less') # older than now

    # Set collection-criterion 'portal-type' to be 'Document':
    criterion = collection.addCriterion('Type', 'ATPortalTypeCriterion')
    criterion.setValue('Document')

    # Set collection-criterion 'relative-path' to be parent,
    # include grand-children and exclude parent in results:
    # criterion = collection.addCriterion('path', 'ATRelativePathCriterion')
    # criterion.setRelativePath('..')
    # criterion.setRecurse(True)

    # Set collection-criterion 'UID-path' to be parent,
    # include grand-children and parent in results:
    criterion = collection.addCriterion('path', 'ATPathCriterion')
    criterion.setValue([collection.aq_parent.UID()])
    criterion.setRecurse(True) # include grand-children

    # Update portal-catalog:
    collection.reindexObject()

