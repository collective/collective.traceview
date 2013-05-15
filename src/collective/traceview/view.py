from zope.interface import implements
from zope.viewlet.interfaces import IViewlet

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

try:
    import oboe
except:
    pass

class TraceviewTopViewlet(BrowserView):
    implements(IViewlet)

    def __init__(self, context, request, view, manager):
        super(TraceviewTopViewlet, self).__init__(context, request)
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager

    def update(self):
        pass

    def render(self):
        """render the Traceview top snippet"""
        try:
            return "<!-- traceview starttag -->" + oboe.rum_header()
        except:
            return ""

class TraceviewButtomViewlet(BrowserView):
    implements(IViewlet)

    def __init__(self, context, request, view, manager):
        super(TraceviewButtomViewlet, self).__init__(context, request)
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager

    def update(self):
        pass

    def render(self):
        """render the Traceview buttom snippet"""
        try:
            return "<!-- traceview endtag -->" + oboe.rum_footer()
        except:
            return ""
