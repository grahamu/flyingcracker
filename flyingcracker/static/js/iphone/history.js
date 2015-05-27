

// 1. app = Title string from each <a> element inside <div id="menuBar">.

    var bookmarkedMenuBarState = YAHOO.util.History.getBookmarkedState("app");
    var initialMenuBarState = bookmarkedMenuBarState || "None";
    YAHOO.util.History.register("app", initialMenuBarState, function (state) {
        // Determine the corresponding URL from anchors in <div id="menuBar">.
        els = get_menubar_links();
        for (i=0; i<len(els); i++)      // BUGBUG - is 'len' correct?
        {
            if (els[i].title == state)
            {
                url = els[i].href;
                // Load that URL as if the user had clicked on the menu item.
                dynamic_navigation(url);
                break;
            }
        }
    });
    
    function get_menubar_links() {
        return YAHOO.util.Dom.getElementsByClassName( 'toolBarLink' , 'a' , 'toolul' );
    }
    
    function handleMenuBarAppChange (e) {
        var el, newState, currentState;

        // get the el for this event
        el = e.target;
        newState = el.title;

        try {
            currentState = YAHOO.util.History.getCurrentState("app");
            if (newState != currentState) {
                // maybe close the menubar?
                YAHOO.util.History.navigate("app", newState);
            }
        } catch (e) {
            // call the function which loads an app
            load_app(newState);     // BUGBUG - why would this ever get called?
                                    //          Write this function?
        }
    }

    function initMenuBar () {
        // find all the <a> menu item elements
        els = get_menubar_links();
        YAHOO.utils.addListener(els, "click", handleMenuBarAppChange);
    }
    

// 2. appState = Whatever data is used for each application.

    var bookmarkedAppState = YAHOO.util.History.getBookmarkedState("appState");
    var initialAppState = bookmarkedAppState || "None";
    YAHOO.util.History.register("state", initialAppState, function (state) {
        // Invoke a Javascript function which should be present for every
        // application. Make sure it exists even if there is no app loaded.
        // Let the app-specific function handle loading the correct stuff.
        app_set_state(state);
    });

    function handleAppStateChange (newState) {
        var currentState;

        try {
            currentState = YAHOO.util.History.getCurrentState("app");
            // The following test is crucial. Otherwise, we end up circling forever.
            // Indeed, YAHOO.util.History.navigate will call the module onStateChange
            // callback, which will call tabView.set, which will call this handler
            // and it keeps going from here...
            if (newState != currentState) {
                YAHOO.util.History.navigate("appState", newState);
            }
        } catch (e) {
            // call a function which changes the application state
            app_set_state(newState);
        }
    }
    
    // Somehow each app needs to have a method of determining when its
    // state changes. When that happens, it needs to call
    // handleAppStateChange(state). This has the effect of adding
    // the state information to the history. Of course then the
    // application-specific app_set_state() function is called
    // to handle actually loading the new content in some fashion.
    //
    // We should look at each application to see how its state
    // can be codified in a string.


// and the initialization:

    // Initialize the browser history management library.
    try {
        YAHOO.util.History.initialize("yui-history-field", "");
    } catch (e) {
        // The only exception that gets thrown here is when the browser is
        // not supported (Opera, or not A-grade) Degrade gracefully.
        
        // I think the initMenuBar func is not needed because the js in iphone_base
        // listens in "god" mode for the click event and sees when a 'toolBarLink' element
        // is clicked on.
        
        initMenuBar();
    }
