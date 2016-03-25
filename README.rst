===================
TraceView for Plone
===================

The *collective.traceview* package adds support for `TraceView`_, aka Tracelytics, to Plone. The full `TraceView documentation`_ can be read for more information.

Contents
========

.. contents::

Introduction
============

TraceView times the full request from the browser through frontend servers to
application servers. collective.traceview gives you insight into Zope/Plone
internals and adds these layers to TraceView:

 * Zope HTTP Server
 * Zope publisher
 * ZODB
 * Portal Transforms
 * Outbound calls to e.g. webservices
 * Portal Catalog searches
 * Chameleon ZPT engine

It also adds tags to the HTML header and footer to instrument TraceView Real User
Monitoring (RUM), so you'll get metrics about user network connectivity and how
long time your site takes to render inside the browsers of the real users.

Requirements
============

You need a TraceView account, TraceView installed on the Plone server. And then the
TraceView Python oboe library must be installed with the same Python that runs Plone.

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
        recipe = plone.recipe.zope2instance
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
in the usual way as described above and set the following environment variables. See example below:

      ::

        [instance]
        recipe = plone.recipe.zope2instance
        ...
        environment-vars =
          ...
          TRACEVIEW_IGNORE_EXTENSIONS js;css;png;jpeg;jpg;gif;pjpeg;x-png;pdf
          TRACEVIEW_IGNORE_FOUR_OH_FOUR 1
          TRACEVIEW_PLONE_TRACING 1
          TRACEVIEW_DETAILED_PARTITION 1
          TRACEVIEW_SAMPLE_RATE 1.0
          TRACEVIEW_TRACING_MODE always

**TRACEVIEW_IGNORE_EXTENSIONS** tells TraceView not to trace urls with the following extensions,
default value no extension is defined.

      ``TRACEVIEW_IGNORE_EXTENSIONS=js;css;png;jpeg;jpg;gif;pjpeg;x-png;pdf``

**TRACEVIEW_IGNORE_FOUR_OH_FOUR** tells TraceView not to record 404 pages, default value is *0*.

      ``TRACEVIEW_IGNORE_FOUR_OH_FOUR=1``

**TRACEVIEW_PLONE_TRACING** tells Plone to do the tracing, do not set this if you have oboe
installed on apache in the front end, default value is *0*.

      ``TRACEVIEW_PLONE_TRACING=1``

**TRACEVIEW_DETAILED_PARTITION** will split trafic into detailed partition, where the partition
name will also include hostname and zope instance name. The default is to only partition for
Anonymous and Authenticated trafic.

      ``TRACEVIEW_DETAILED_PARTITION=1``

**TRACEVIEW_SAMPLE_RATE** the sample rate, *1.0* means all requests, *0.0* means no requests,
default value is *0.3*.

      ``TRACEVIEW_SAMPLE_RATE=1.0``

**TRACEVIEW_TRACING_MODE** tracing mode, *always* means that we will trace requests, none means no requests to be traced,
default value is *none*.

      ``TRACEVIEW_TRACING_MODE=always``

.. _TraceView: http://docs.appneta.com/platform-and-component-support#python-frameworks
.. _TraceView documentation: http://docs.appneta.com/traceview
