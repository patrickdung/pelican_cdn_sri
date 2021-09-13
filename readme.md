Pelican plugin for faster and safer use of CDN resources
--------------------------------------------------------

This plugin queries two major CDN services (CDNJS and jsDelivr only).
Also this plugin supports use of either css or js file only.
The user provide information about which application and the version
that they want to use. The plugin queries the API of the CDN and
return a code block that could be used in the Pelican template.
The code block would include the SRI hash.
This save time for the users and is secure than just using the latest version
of an application and do not use SRI.

This plugin references several Pelican plugins. So this plugin
would be in AGPLv3.

- [Pelican Plugins](https://github.com/getpelican/pelican-plugins/)
- [pelican-webmention](https://github.com/drivet/pelican-webmention)
- [webmention_static_kappa](https://github.com/kappa-wingman/webmention_static_kappa)

Parameters to be added for using this plugin
--------------------------------------------

Parameters are: CDN_SRI, CDN_SRI_OVERWRITE_INITIAL_CACHE, CDN_SRI_UPDATE_INITIAL_CACHE, CDN_SRI_CACHE_FILENAME

- CDN_SRI, example:
```
CDN_SRI = {
    'bootstrap': {
        'cdn_type': 'cdnjs',
        'version': '5.1.1',
        'css': 'css/bootstrap.min.css',
        'js': 'js/bootstrap.min.js',
    },
    'docs-searchbar.js': {
        'cdn_type': 'jsdelivr',
        'version': '1.3.2',
        'css': 'dist/cdn/docs-searchbar.min.css',
        'js': 'dist/cdn/docs-searchbar.min.js',
    },
}
```

- This is the location of the cache file:
  - CDN_SRI_CACHE_FILENAME = './cdn-sri-cache/cache.json'
  - You need to create a directory called 'cdn-sri-cache' in the same directory as your Peclian directory
  - For first time use, you should set 'CDN_SRI_OVERWRITE_INITIAL_CACHE' to true or create an (empty, content is {}) cache.json file

- You need to set overwrite/update the initial cache to True.
  If there are any changes in the version of the web applications
  - CDN_SRI_OVERWRITE_INITIAL_CACHE = False
  - CDN_SRI_UPDATE_INITIAL_CACHE = True

How to use it in the template
-----------------------------

With reference to the above example, the user could specify:
{{ BOOTSTRAP_CSS }} to generate a code block for Bootstrap css.
So the format is {{ APPLICTION_NAME_CSS }} .
Note you need to replace '-' and '.' with '_' for the application name.
The generated code block is:

```
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.1/css/bootstrap.min.css" integrity="sha512-6KY5s6UI5J7SVYuZB4S/CZMyPylqyyNZco376NM2Z8Sb8OxEdp02e1jkKk/wZxIEmjQ6DRCEBhni+gpr9c4tvA==" crossorigin="anonymous" referrerpolicy="no-referrer">
```

So, the format for using the JS docs searchbar in the above example would be:
{{ DOCS_SEARCHBAR_JS_JS }}.
The first '_JS' is there because the application name is called docs-searchbar.js
The last '_JS' is specifying that we want to use the JavaScript code block.
If you want to use the CSS of the docs-searchbar.js, then it would be:
{{ DOCS_SEARCHBAR_JS_CSS }}.

License
-------
Unless the folder itself contains a LICENSE stating otherwise, all the files
distributed here are released under the GNU AFFERO GENERAL PUBLIC LICENSE.
