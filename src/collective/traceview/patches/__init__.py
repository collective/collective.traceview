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
    import publisher
    import catalog
    import zodbpatch
    import memoize
    import viewletmanagers
    #import template
    if is_recent_python:
        import transform
    

