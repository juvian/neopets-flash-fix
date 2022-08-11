# How to play most flash games

1. Do Waterfox steps from [this reddit post](https://www.reddit.com/r/neopets/comments/s7jzyt/how_to_enable_flash_post_endoflife/)
2. Install [Fiddler Classic](https://www.telerik.com/download/fiddler) (if mac, try [virtual machine](https://docs.telerik.com/fiddler/configure-fiddler/tasks/configureformac) or [proxyman](proxyman))
3. Open fiddler, go to rules -> customize rules
4. Search for `static function OnBeforeRequest(oSession: Session) {` and add below 

```
if ((oSession.uriContains("neopets.com/crossdomain.xml") || oSession.uriContains("neopets.com") && oSession.HTTPMethodIs("POST")) && !oSession.isHTTPS) {
    oSession.oRequest.headers.UriScheme = "https";
}

```
5. Save (ctrl + s or file -> save). Close ScriptEditor
6. In fiddler go to Tools -> Options -> HTTPS -> make sure capture https connect, decrypt https traffic and ignore server certificate errors are enabled. Restart fiddler
7. Open game in neo (and always keep fiddler open) 

## Extra rules that are good to add
```
if (oSession.uriContains("neopets") && oSession.uriContains(".swf")) {
    oSession.host = "images.neopets.com";
    oSession.url = oSession.url.Replace("/games/https://images.neopets.com/games/", "/games/").Replace("games/games", "games"); 
}
```

This fixes issues with a few games like [Clara on Ice](https://www.neopets.com/games/game.phtml?game_id=1172&size=regular&quality=high&play=true) and [Let it Slide](https://www.neopets.com/games/game.phtml?game_id=970&size=regular&quality=high&play=true)

## Playing newer games

That will work with most games, as it will fix main issues about neo returning 301 status code to redirect to https (which doesn't support POST) instead of 308 (which does) + some crossdomain.xml calls don't work with redirect.
A good way to test if it is working is [Meerca Chase 2](https://www.neopets.com/games/game.phtml?game_id=500&size=regular&quality=high&play=true)

Still, some games have further issues like [Assignment 53](https://www.neopets.com/games/game.phtml/?game_id=1347&size=regular&quality=high&play=true). These kind of newer games have hardcoded in flash code to check if its running on "live" or "offline" aka dev server. This check is done comparing url in which game was loaded against `http://www.neopets.com`. As url now is always https it will never match and thus will assume its the offline mode. This offline mode means it will take no info from page parameters like language and your username and it will do some calls to dev server instead of regular server, which won't work. For these games extra setup is needed on a game to game basis. You will need to download [fixed swf](/fixed-swf) version (where I replace the http for https) and create a rule to replace neo sfw with this fixed one.

![image](https://user-images.githubusercontent.com/5660396/184058059-5d0b1601-ecdb-44af-a0d8-de48a0b5f3b9.png)

In the AutoResponder section, first enable rules and make sure unmatched requests passthrough is checked. Then click add rule and input `EXACT:https://images.neopets.com/games/g1347_v66_45083.swf` and then in the second box click the dropdown arrow and find file. Then browse your pc for the fixed swf file.

## Playing newer games alternative

If you don't want to setup a fix for each broken game or don't want to trust using a modified swf, you can still play games with a few extra rules. However, score sending won't work. Add these rules that fix most issues with using dev server instead of regular:

```
if (oSession.uriContains("dev.neopets.com") && oSession.HTTPMethodIs("POST")) {
    oSession.host = "www.neopets.com";
    if (oSession.uriContains("gettranslationxml.phtml")) {
        oSession.oRequest.headers.HTTPMethod = "GET";
        oSession.fullUrl += '?' + oSession.GetRequestBodyAsString();
    }
}

if (oSession.uriContains("gettranslationxml.phtml")  && oSession.HTTPMethodIs("GET")) {
    oSession.fullUrl = oSession.fullUrl.replace("lang=ch", "lang=en");
}
```



