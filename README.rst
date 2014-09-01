===================
Traceview for Plone
===================

The collective.traceview package adds support for Traceview (aka Tracelytics) to Plone.

Contents
========

.. contents::

Introduction
============

Traceview times the full request from the browser through frontend servers to
application servers. collective.traceview gives you insight into Zope/Plone
internals and adds these layers to Traceview:

 * Zope HTTP Server
 * Zope publisher
 * ZODB
 * Portal Transforms
 * Outbound calls to e.g. webservices
 * Portal Catalog searches
 * Chameleon ZPT engine

It also adds tags to the HTML header and footer to instrument Traceview Real User
Monitoring (RUM), so you'll get metrics about user network connectivity and how
long time your site takes to render inside the browsers of the real users.

Requirements
============

You need a Traceview account, Traceview installed on the Plone server. And then the
Traceview Python oboe library must be installed with the same Python that runs Plone.

collective.traceview has been tested with Plone 4.

System dependencies: liboboe and liboboe-devel (for CentOS) or liboboe-dev (for Debian/Ubuntu)


How to install
==============

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


Plone tracing (NEW)
===================

Usually the X-Trace header is generated from a front-end webserver, typically apache. But
in some cases there is no such front-end webserver, so nowhere to start the trace. We
did now add the possibility to get Plone to start the tracing. Just install the product
in the usual way as described above and set the following environment variables.

* ``TRACEVIEW_IGNORE_EXTENSIONS=js;css;png;jpeg;jpg;gif;pjpeg;x-png;pdf``

  Tells traceview not to trace urls with the following extensions.

* ``TRACEVIEW_IGNORE_FOUR_OH_FOUR=1``

  Tells traceview not to record 404 pages.

* ``TRACEVIEW_PLONE_TRACING=1``

  Tells Plone to do the tracing, do not set this if you have oboe installed on apache in
  the front end.

* ``TRACEVIEW_SAMPLE_RATE=1.0``

  The sample rate, 1.0 means all requests, 0.0 means no requests.

* ``TRACEVIEW_TRACING_MODE=always``

  Tracing mode, always means that we will trace requests, none means no requests to be traced.
