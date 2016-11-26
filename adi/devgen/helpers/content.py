# -*- coding: utf-8 -*-

# Terminology and Manifesto:
# A child is any site's content-item.
# A child can be a parent of children.
# A site is the uppest parent, it cannot be a child,
# allthough in reality, it is a child of ZOPE.
# A ZOPE is a child in time.

from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from adi.commons.commons import iterToTags
from adi.commons.commons import newlinesToTags


def addChild(parent, id_, typ='Folder', FIRE=False):
    """
    Add child to parent and return it, unless child exists already, then return
    existing child. If FIRE is True, use 'invokeFactory()', which triggers
    firing of events, like when done manually by a user. Otherwise use
    `_createObjectByType()`, which does not fire events.
    Sets a child's id as default-title, so something shows up in folder-listings.
    """
    child = None
    if not idExistsInSite(parent, id_):
        if FIRE:
            parent.invokeFactory(typ, id_)
            child = parent[id_]
        else:
            child = _createObjectByType(typ, parent, id_)
        child.setTitle(id_)
        child.reindexObject()
    else: child = parent[id_]
    return child

def addChildren(parent, ids, typ='Folder'):
    """ For each id execute addChild()."""
    children = []
    for id_ in ids:
        child = addChild(parent, id_)
        if child: children.append(child)
    return children

def addNChildren(parent, n, typ='Folder'):
    """
    For quick population, passing ids is not needed:
    Add n-children, each getting its nr as id.
    """
    children_ids = []
    while n > 0:
        children_ids.append(str(n))
        n -= 1
    children = addChildren(parent, children_ids, typ='Folder')
    return children

def addNChildrenRecursive(parent, n=3, container_id='0', max_depth=4):
    """
    Add x children, in them add x children, repeat
    this x-times and wrap in container with id '0'.
    Fails silently, if container_id exists already.
    Should result in x**x children with deepest paths,
    e.g. if x is two, you get a tree like:

        0
     1     2
    1 2   1 2       ---> deepest-path-children == x**x

    """
    if n > max_depth: exit("""

A factor greater than """ + max_depth + """ takes a long
time and might bring your disc-space-consumption to its
limit. Aborting now, nothing changed. You might change
max_depth, but remember this grows exponentially, so thy
had been warned: Beyond there may be porcupines!
Tested with factor five, results in 100MB.

""")
    # Add root-item:
    parent = addChild(parent, container_id)
    first_children = [parent]
    second_children = []
    depth = 0
    # Populate children until reaching deepest level: 
    while depth < n:
        # Make each child the parent to fill, one after another:
        parent = first_children.pop(0)
        children_ids = range(n + 1)[1:] # start with 1 not 0, for dem humans
        # Collect the added childs to the next generation first-childs:
        second_children += addChildren(parent, children_ids)
        # All first level children have been filled and removed of list:
        if len(first_children) == 0:
            # Refill first_children-list with second_children:
            first_children = second_children
            second_children = [] # clear
            # Raise while-loop-end-condition:
            depth +=1

def childExists(parent, child_id):
    if idExistsInParent(child_id): return True
    else: return False

def getAllChildren(parent):
    children = []
    for i in parent.portal_catalog():
        children.append(i)
    return children

def getChildren(parent):
    return parent.getFolderContents()

def getChildrenOfType(parent, typ):
    return parent.listFolderContents({'portal_type':typ})

def getChildBrainById(parent, id_):
    return parent.portal_catalog(id=id_)[0][0]

def getChildDepthInSite(context):
    return len( context.getPhysicalPath() ) - 2

def getChildPath(child):
    return '/'.join(child.getPhysicalPath())

def getChildPosInParent(child):
    """
    Get child position in parent as a number, return None, if not found.
    """
    nr = 0
    if not isSite(child):
        parent = child.aq_parent
        siblings = parent.getFolderContents()
        for sibling in siblings:
            nr += 1
            if sibling['id'] == child.id:
                return nr
    return nr

def getChildPosInParents(child):
    """
    Get child position in parents as a dot-separated string of numbers,
    like e.g.: '1.2.7' (= 7th child of 2nd child of 1st child of site).
    """
    nrs = ''
    while not isSite(child):
        nrs = str( getChildPosInParent(child) ) + '.' + nrs
        child = child.aq_parent
    nrs = nrs[:-1]
    return nrs

def getField(context, field_name):
    """
    Return value of field as a string.
    """
    return context.Schema()[field_name]

def getFields(context, field_names=None):
    """
    Return all fields of an archetype based content-item
    as a list of key/value-pairs-sequence, as strings, e.g.:
    ['title', 'Welcome', 'creation_date', '2016/07/08 19:03:33.607601 GMT+2']
    Filter by field_names if passed, return results in same order.
    Fail silently, if context is not an archetype, e.g. on the siteroot.
    """
    pairs = []
    if context.Schema(): # is archetype
        schema = context.Schema()
        fields = schema.fields()
        if field_names:
            for field_name in field_names:
                val = None
                pairs.append(schema[field_name].getName())
                val = schema[field_name].get(context)
                if isinstance(val, tuple) or isinstance(val, list):
                    val = iterToTags(val)
                elif str(val).find('\n') != -1:
                    val = newlinesToTags(val)
                pairs.append(val)
        else:
            for field in fields:
                val = None
                pairs.append(field.getName())
                val = str(field.get(context))
                if val.find('\n') != -1:
                    val = newlinesToTags(val)
                pairs.append(val)
    return pairs

def getParentPath(child):
    return '/'.join(child.getPhysicalPath()[:-1])

def getSiteId(child):
    return child.getPhysicalPath()[1]

def getSitePath(child):
    return '/'.join(child.getPhysicalPath()[:1])

def getUserId(child):
    return str(child.portal_membership.getAuthenticatedMember())

def hasChildren(parent):
    if len(getChildren(parent)) > 0: return True
    else: return False

def hasField(child, field_name):
    if field_name in dir(child): return True
    else: return False

def idExists(item, id_):
    """Short form for idExistsInSite()."""
    return idExistsInSite(item, id_)

def idExistsInParent(parent, id_):
    if id_ in parent.keys(): return True
    else: return False

def idExistsInParentFamily(parent, id_):
    """Include grand-children in search."""
    path = getChildPath(parent)
    return idExistsInPath(parent, id_, path)

def idExistsInPath(child, id_, path):
    results = child.portal_catalog(path=path, id=id_)
    if results:
        results = results[0]
        if len(results) > 0: return True
        else: return False
    else: return False

def idExistsInSite(item, id_):
    """Return bool indicating whether id exists in site, or not."""
    results = item.portal_catalog(id=id_)
    if len(results) > 0: return True
    else: return False

def idIsUnique(child, id_):
    results = child.getSite().portal_catalog(id=id_)
    if len(results) == 1: return True
    else: return False

def isSite(context):
    if len( context.getPhysicalPath() ) == 2: return True
    else: return False

def isSiteFirstChild(child):
    if len( child.getPhysicalPath() ) == 3: return True
    else: return False

def isZope(context):
    if len( context.getPhysicalPath() ) == 1: return True
    else: return False

