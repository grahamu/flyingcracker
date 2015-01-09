#!/usr/bin/env python
from django.contrib import admin
import blog.models as blog
from fc3.settings.base import YUI_VERSION, STATIC_URL


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'author', 'pub_date']
    search_fields = ['title', 'body']
    date_hierarchy = 'pub_date'

    class Media:
#        js = [STATIC_URL+'js/tiny_mce/tiny_mce.js', STATIC_URL+'js/textareas.js']
        js = (
            # Utility dependencies
            'http://yui.yahooapis.com/'+YUI_VERSION+'/build/yahoo-dom-event/yahoo-dom-event.js',
            'http://yui.yahooapis.com/'+YUI_VERSION+'/build/element/element-min.js',
            # Needed for Menus, Buttons and Overlays used in the RTE Toolbar
            'http://yui.yahooapis.com/'+YUI_VERSION+'/build/container/container_core-min.js',
            'http://yui.yahooapis.com/'+YUI_VERSION+'/build/menu/menu-min.js',
            'http://yui.yahooapis.com/'+YUI_VERSION+'/build/button/button-min.js',
            # Source file for Rich Text Editor
            'http://yui.yahooapis.com/'+YUI_VERSION+'/build/editor/editor-min.js',
            # Source file for Connection Manager
#            'http://yui.yahooapis.com/'+YUI_VERSION+'/build/connection/connection-min.js',
            STATIC_URL+'js/yui/connection-debug.js',
            # Required for YUI Logger
            'http://yui.yahooapis.com/'+YUI_VERSION+'/build/logger/logger-min.js',
            # Enable console logging
            STATIC_URL+'js/console-logger.js',
            # Image uploader code
            STATIC_URL+'js/yui-image-uploader.js',
            # Invoke the RTE
            STATIC_URL+'js/yuitextareas.js',
            )

admin.site.register(blog.Post, PostAdmin)
