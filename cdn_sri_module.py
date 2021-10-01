# -*- coding: utf-8 -*-

# SPDX-License-Identifier: AGPL-3.0-only
#
# Copyright (c) 2021 Patrick Dung

import os, urllib.request, json

global cdn_api_url, cdn_api_url_parameters, cdn_result

cdn_api_url = {
    'cdnjs': 'https://api.cdnjs.com/libraries',
    'jsdelivr': 'https://data.jsdelivr.com/v1/package/npm',
}

cdn_api_url_parameters = {
    'cdnjs': '?fields=sri',
    'jsdelivr': '',
}

# For jsdelivr only
def search_files_in_dict (dict1, search_item_name):
  for i in dict1['files']:
    if i['name'] == search_item_name:
      return i

def query_cdn_api(CDN_SRI):

  cdn_result = {}

  for cdn_item in CDN_SRI:
    this_cdn_type=CDN_SRI[cdn_item]['cdn_type']

    #print ("DEBUG1", cdn_item);
    if this_cdn_type == 'cdnjs':
      cdn_item_api_url=(cdn_api_url[this_cdn_type]+'/'+cdn_item+'/'+CDN_SRI[cdn_item]['version']+cdn_api_url_parameters[this_cdn_type])
      #print ("DEBUG2", cdn_item_api_url)

      try:
        response = urllib.request.urlopen(cdn_item_api_url)
        data = response.read().decode("utf-8")
        incoming_json = json.loads(data)
      except:
        raise

      #print ("DEBUG3", str(incoming_json))

      for filelist_injson in incoming_json['sri']:

        cdn_item_src = "https://cdnjs.cloudflare.com/ajax/libs/"+cdn_item+"/"+CDN_SRI[cdn_item]['version']+"/"+filelist_injson
        cdn_item_hash = str(incoming_json['sri'][filelist_injson])

        if ('css' in CDN_SRI[cdn_item]) and (CDN_SRI[cdn_item]['css'] == filelist_injson):
             cdn_script_block = '<link rel="stylesheet" href="' +cdn_item_src+ '" integrity="' +cdn_item_hash+ '" crossorigin="anonymous" referrerpolicy="no-referrer">'
             #cdn_result.setdefault(cdn_item,[]).append ({'css':cdn_script_block})
             #print (cdn_result)
             cdn_result[cdn_item+'_css']=(cdn_script_block)

        if ('js' in CDN_SRI[cdn_item]) and (CDN_SRI[cdn_item]['js'] == filelist_injson):
             cdn_script_block = '<script src="' +cdn_item_src+ '" integrity="' +cdn_item_hash+ '" crossorigin="anonymous" referrerpolicy="no-referrer"></script>'
             #cdn_result.setdefault(cdn_item,[]).append ({'js':cdn_script_block})
             cdn_result[cdn_item+'_js']=(cdn_script_block)

    elif (this_cdn_type == 'jsdelivr'):
      cdn_item_api_url=(cdn_api_url[this_cdn_type]+'/'+cdn_item+'@'+CDN_SRI[cdn_item]['version']+cdn_api_url_parameters[this_cdn_type])
      #print (cdn_item_api_url)

      try:
        response = urllib.request.urlopen(cdn_item_api_url)
        data = response.read().decode("utf-8")
        incoming_json_jsdelivr = json.loads(data)
        #print (str(incoming_json_jsdelivr))
      except:
        raise

      for i in incoming_json_jsdelivr['files']:
        cdn_item_src = "https://cdn.jsdelivr.net/npm/"+cdn_item+"@"+CDN_SRI[cdn_item]['version']

        is_found = False
        if ('css' in CDN_SRI[cdn_item]):
          tokenized_source_url = CDN_SRI[cdn_item]['css'].split("/")
          #print (tokenized_source_url)
          #print (i['name'])
          j=i
          if j['name'] == tokenized_source_url[-1]:
            #print ( "DEBUG2" , j['name'], tokenized_source_url[-1])
            is_found=True
          elif (j['name']==(tokenized_source_url.pop(0)) ):
            #print ( "DEBUG3" , j['name'], tokenized_source_url[-1])
            for token in tokenized_source_url:
              j=(search_files_in_dict (j, token))
              #print ("DEBUG4",(j))
              if j['name'] == tokenized_source_url[-1]:
                is_found=True
                print (j,"css found")

          if (is_found):  
            cdn_item_hash="sha256-" + j['hash']
            cdn_script_block = '<link rel="stylesheet" href="' +cdn_item_src+ '/' + CDN_SRI[cdn_item]['css'] + '" integrity="' +cdn_item_hash+ '" crossorigin="anonymous" referrerpolicy="no-referrer">'
            #cdn_result.setdefault(cdn_item,[]).append ({'css':cdn_script_block})
            cdn_result[cdn_item+'_css']=(cdn_script_block)

        is_found = False
        if ('js' in CDN_SRI[cdn_item]):
          tokenized_source_url = CDN_SRI[cdn_item]['js'].split("/")
          #print ('js', tokenized_source_url)
          #print (i['name'])
          j=i
          if j['name'] == tokenized_source_url[-1]:
            is_found=True
          elif (j['name']==(tokenized_source_url.pop(0)) ):
            for token in tokenized_source_url:
              j=(search_files_in_dict (j, token))
              #print ("DEBUG",(j))
              if j['name'] == tokenized_source_url[-1]:
                is_found=True
                print (j,"js found")

          if (is_found):  
            cdn_item_hash="sha256-" + j['hash']
            cdn_script_block = '<script src="' +cdn_item_src+ '/' + CDN_SRI[cdn_item]['js'] + '" integrity="' + cdn_item_hash+ '" crossorigin="anonymous" referrerpolicy="no-referrer"></script>'
            #cdn_result.setdefault(cdn_item,[]).append ({'js':cdn_script_block})
            cdn_result[cdn_item+'_js']=(cdn_script_block)

    # endof: if cdntype is jsdelivr

  return (cdn_result)
