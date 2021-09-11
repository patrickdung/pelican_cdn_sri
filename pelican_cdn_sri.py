# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os, urllib.request, json

from pelican import signals, contents, generators, settings
from pelican.contents import Content, Article
from pelican.settings import DEFAULT_CONFIG

from .cdn_sri_module import query_cdn_api

"""
  This plugin is for getting the CDN script tag blocks (with SRI) to use in template
"""

def initialize_module(pelican):

    global CDN_SRI, CDN_SRI_OVERWRITE_INITIAL_CACHE, CDN_SRI_UPDATE_INITIAL_CACHE, CDN_SRI_CACHE_FILENAME

    for parameter in [ 'CDN_SRI', 'CDN_SRI_OVERWRITE_INITIAL_CACHE', 'CDN_SRI_UPDATE_INITIAL_CACHE', 'CDN_SRI_CACHE_FILENAME' ]:
      if not parameter in pelican.settings.keys():
          print ("cdn_sri error: no " + parameter + "defined in settings")
      else:
        globals()[parameter] = pelican.settings.get(parameter)
        ##globals()[parameter] = pelican.settings[parameter]
        ##print (globals()[parameter])

    if CDN_SRI_OVERWRITE_INITIAL_CACHE:
        overwrite_initial_cache ()

    if CDN_SRI_UPDATE_INITIAL_CACHE:
        update_initial_cache ()

    try:
        #data = json.dumps(get_cdn_sri_result())
        file = open(CDN_SRI_CACHE_FILENAME, "r")
        #incoming_json = json.loads(data)
        incoming_json = json.load(file)
        file.close()
        #print ('PDEBUG1', incoming_json)
        for k, v in incoming_json.items():
          #print ('PDEBUG2', k,v)
          pelican.settings.setdefault('CDNSRI_'+str(k).upper().replace("-","_").replace(".","_") ,v)
    except:
      raise

def overwrite_initial_cache ():
    try:
        data = json.dumps(get_cdn_sri_result())
        file = open(CDN_SRI_CACHE_FILENAME, "w+")
        file.write(data)
        file.close()
    except:
        raise

def update_initial_cache ():
    try:
        file = open(CDN_SRI_CACHE_FILENAME, "r")
        cached_json = json.load(file)
        file.close()
    except:
        raise

    if cached_json is None:
        cached_json = {}

    try:
        data = json.dumps(get_cdn_sri_result())
        incoming_json = json.loads(data)
    except:
        raise
    cached_json.update(incoming_json)
    #print (cached_json)
    try:
        file = open(CDN_SRI_CACHE_FILENAME, "w+")
        json.dump(cached_json, file)
        file.close()
    except:
        raise

def get_cdn_sri_result():
  cdn_result = query_cdn_api(CDN_SRI)
  #print("PDEBUG 3", cdn_result)

  return (cdn_result)

def register():
    ## only need to add to the global before writing article/pages/templates
    signals.initialized.connect(initialize_module)

    ## only works for articles
    ##signals.article_generator_context.connect(setup_cdn_sri)
    ##signals.article_generator_write_article.connect(fetch_cdn_sri)
    # add metadata to all articles/pages/templates
    # but unable to retrieve the meta for direct templates
    ##signals.all_generators_finalized.connect(setup_content_cdn_sri)
