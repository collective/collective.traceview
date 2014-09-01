import sys
if sys.version_info >= (2, 6):
    is_recent_python = True
else:
    is_recent_python = False

try:
    import oboeexception
    from oboeware import loader
    if is_recent_python:
        loader.load_inst_modules()
except:
    import logging
    logger = logging.getLogger("Plone")
    logger.warn("Could not import oboeware, no tracing is done.")
    pass
else:
    import httpserver
    import publisher
    import catalog
    import zodbpatch
    import memoize
    import viewletmanagers

    try:
        import chameleonpatch
    except ImportError:
        import logging
        logger = logging.getLogger("Plone")
        logger.warn("Could not patch Chameleon, if it is installed there is a problem")
        pass

    if is_recent_python:
        import transform
