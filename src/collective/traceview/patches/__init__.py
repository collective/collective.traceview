try:
    import oboeexception
    from oboeware import loader
    loader.load_inst_modules()
except:
    import logging
    logger = logging.getLogger("Plone")
    logger.warn("Could not import oboeware, no tracing is done.")
    pass
else:
    #import httpserver
    import publisher
    import catalog
    import transform
    import zodb
    import memoize
    import viewletmanagers
    #import template

