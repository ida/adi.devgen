# This file is about ZOPE's event-machinery, which fires events on certain occasions,
# it is *not* about the content-type 'Event.

# See also:
# http://docs.plone.org/external/plone.app.dexterity/docs/advanced/event-handlers.html

# Additional notes to the official docs:

# zope.lifecycleevent.interfaces.IObjectAddedEvent
# Will be fired five times!
# Two times on initialization (add), three times on finalization (save).

