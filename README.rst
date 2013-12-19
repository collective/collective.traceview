Traceview for Plone
===================

The collective.traceview package adds support for Traceview (aka Tracelytics) to Plone.

Traceview times the full request from the browser through frontend servers to
application servers. collective.traceview gives you insight into Zope/Plone
internals and adds these layers to Traceview:

 * Zope http server
 * Zope publisher
 * ZODB
 * Portal Transforms
 * Outbound calls to e.g. webservices
 * Portal Catalog searches

It also adds tags to the HTML header and footer to instrument Traceview Real User
Monitoring (RUM), so you'll get metrics about user network connectivity and how
long time your site takes to render inside the browsers of the real users.


Requirements
------------

You need a Traceview account, Traceview installed on the Plone server. And then the
Traceview Python oboe library must be installed with the same Python that runs Plone.

collective.traceview has been tested with Plone 4.

System dependencies: liboboe and liboboe-devel (for CentOS) or liboboe-dev (for Debian/Ubuntu)


How to install
--------------

Update your ``buildout.cfg`` file:

* Add tracelytics pypi under ``find-links``

      ::

        find-links += http://pypi.tracelytics.com/oboe

* Add package in develop mode

      ::

        auto-checkout = collective.traceview

* Add ``oboe`` and ``collective.traceview`` to the list of eggs to install

      ::

        [instance]
        ...
        eggs =
          ...
          collective.traceview
          oboe

* Get package from collective sources (or create your own GitHub fork)

      ::

        [sources]
        ...
        collective.traceview = git https://github.com/collective/collective.traceview.git

* Get ``oboe`` egg version 1.3.8, the latest one released on pypi (version 1.4.2) is not yet fully tested (RUM not working)

      ::

        [versions]
        ...
        oboe = 1.3.8

Re-run buildout, e.g. with:

      ``$ ./bin/buildout``

