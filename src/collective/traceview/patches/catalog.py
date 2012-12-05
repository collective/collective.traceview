import oboe


def extract_count(func, f_args, f_kwargs, res):
    return {'Count': len(res)}

from Products.CMFPlone.CatalogTool import CatalogTool
CatalogTool.orig_searchResults = CatalogTool.searchResults

zc_wrapper = oboe.log_method('plone_zcatalog', store_args=True,
                             store_backtrace=True, callback=extract_count)
CatalogTool.searchResults = zc_wrapper(CatalogTool.orig_searchResults)
