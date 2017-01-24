# This file is about ZOPE's event-machinery, which fires events on certain occasions,
# it is *not* about the content-type 'Event'. See also:
# http://docs.plone.org/external/plone.app.dexterity/docs/advanced/event-handlers.html
#
# ADD
# ===
# Additional notes to the official docs:
# zope.lifecycleevent.interfaces.IObjectAddedEvent
# Will be fired five times!
# Two times on initialization (add), three times on finalization (save),
# when added via UI. When added via invokeFactory() of a script, will be
# fired only two times.
#
# When creating and hitting Return-key, we get the err-msg in UI and this
# event will also be fired two times here!
#
# Anytime this event gets fired, the obj has a new id.



# EDIT
# ====
# Example edit-events, in configure.zcml, insert:
  <!--  An edit has been started: -->
  <subscriber for="* Products.Archetypes.interfaces.IEditBegunEvent"
   handler=".subscriber.doAfterEditStart" />
  <!--  An edit has been saved: -->
  <subscriber for="* Products.Archetypes.interfaces.IObjectEditedEvent"
   handler=".subscriber.doAfterEditSave" />
  <!--  An edit has been canceled: -->
  <subscriber for="* Products.Archetypes.interfaces.IEditCancelledEvent"
   handler=".subscriber.doAfterEditCancel" />
# In subscriber.py, insert:
# def doAfterEditStart(obj, eve): pass # do sth
