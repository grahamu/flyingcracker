
function Set_Cookie( name, value, expires, path, domain, secure ) 
{
    // set time, it's in milliseconds
    var today = new Date();
    today.setTime( today.getTime() );
    
    /*
    if the expires variable is set, make the correct 
    expires time, the current script below will set 
    it for x number of days, to make it for hours, 
    delete * 24, for minutes, delete * 60 * 24
    */
    if ( expires )
    {
    expires = expires * 1000 * 60 * 60 * 24;
    }
    var expires_date = new Date( today.getTime() + (expires) );
    
    document.cookie = name + "=" +escape( value ) +
    ( ( expires ) ? ";expires=" + expires_date.toGMTString() : "" ) + 
    ( ( path ) ? ";path=" + path : "" ) + 
    ( ( domain ) ? ";domain=" + domain : "" ) +
    ( ( secure ) ? ";secure" : "" );
}

function load_lib(libname, libpath, initfunc) {
    onerror=null;
    alert("starting load_lib");
    var loader = new YAHOO.util.YUILoader();
    loader.addModule(
        {
            name: libname,
            type: "js",
            fullpath: libpath,
            //requires: ['yahoo', 'dom', 'event', 'connection', 'json'],
            varName: "boogie"
        }
    );
    loader.onSuccess = function() {
                setTimeout(initfunc, 1000);
            };
            
    loader.onFailure = function() {
                alert("YUILoader failure");
            };
    
    loader.insert();
}