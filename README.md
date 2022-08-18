# How to play most flash games

## With Mitmproxy
1. Install Waterfox from [this reddit post](https://www.reddit.com/r/neopets/comments/s7jzyt/how_to_enable_flash_post_endoflife/) if you want to play use flash. For shickwave/3dvia just need IE or chrome + IE tab
2. In waterfox go to about:config then search security.enterprise_roots.enabled and change it to true
3. In waterfox go to about:preferences then search for proxy then click on settings and Set Manual proxy configuration to 127.0.0.1 with port 8080. Make sure to also check use this proxy for FTP and HTTPs

![image](https://user-images.githubusercontent.com/5660396/185045695-d6c32114-e096-4533-8e16-1e0eaaadfa66.png)

4. Install [Mitmproxy](https://mitmproxy.org/)
5. Download [addon](/mitmproxy/neopets.py)
6. Find mitmproxy installation path, go to mitmproxy/addons folder, create a neopets folder and put the neopets.py file inside it (something like C:\Program Files\mitmproxy\bin\mitmproxy\addons\neopets)
7. Find mitmproxy installation path, create a shortcut out of mitmdump.exe. Right click shortcut -> properties -> add -s mitmproxy\addons\neopets\neopets.py to the end of target (should end up like "C:\Program Files\mitmproxy\bin\mitmdump.exe" -s mitmproxy\addons\neopets\neopets.py). Click apply
8. Run mitmproxy (double click shortcut)
9. Go to [http://mitm.it/](http://mitm.it/). Show instructions and install certificate 
10. Go to neopets and hopefully all works

### Extra
TODO

## With Fiddler

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
if (oSession.uriContains("neopets") && (oSession.uriContains(".swf") || oSession.uriContains("/config.xml"))) {
    oSession.host = "images.neopets.com";
    oSession.url = oSession.url.Replace("/games/https://images.neopets.com/games/", "/games/").Replace("games/games", "games"); 
}
```

This fixes issues with a few games like [Clara on Ice](https://www.neopets.com/games/game.phtml?game_id=1172&size=regular&quality=high&play=true), [Let it Slide](https://www.neopets.com/games/game.phtml?game_id=970&size=regular&quality=high&play=true) and [Extreme Potato Counter
](https://www.neopets.com/games/game.phtml?game_id=226&size=regular&quality=high&play=true)

```
if (oSession.uriContains("virtools.download.akamai.com/6712/player/install/")) {
  oSession.fullUrl = "https://3dlifeplayer.dl.3dvia.com/" + oSession.url.Substring(oSession.url.lastIndexOf("player/install"));		
}
```

This fixes 3dvia games like [Terror Mountain Tilt](https://www.neopets.com/games/game.phtml?game_id=925&size=regular&quality=high&play=true). Note that these don't work in waterfox and you need IE or chrome, follow [these instructions](https://www.youtube.com/watch?v=NH8WfY7MvU4)

```
if (oSession.uriContains("shellconfig.xml") && oSession.HostnameIs("www.neopets.com")) {
  oSession.host = "images.neopets.com";
}
```

This fixes issues with newer games

## Playing newer games

That will work with most games, as it will fix main issues about neo returning 301 status code to redirect to https (which doesn't support POST) instead of 308 (which does) + some crossdomain.xml calls don't work with redirect.
A good way to test if it is working is [Meerca Chase 2](https://www.neopets.com/games/game.phtml?game_id=500&size=regular&quality=high&play=true)

Still, some games have further issues like [Assignment 53](https://www.neopets.com/games/game.phtml/?game_id=1347&size=regular&quality=high&play=true) and [Coal Wars](https://www.neopets.com/games/game.phtml?game_id=1370&size=regular&quality=high&play=true). These kind of newer games have hardcoded in flash code to check if its running on "live" or "offline" aka dev server. This check is done comparing url in which game was loaded against `http://www.neopets.com`. As url now is always https it will never match and thus will assume its the offline mode. This offline mode means it will take no info from page parameters like language and your username and it will do some calls to dev server instead of regular server, which won't work. For these games extra setup is needed on a game to game basis. You will need to download [fixed swf](/fixed-swf) version (where I replace the http for https) and create a rule to replace neo sfw with this fixed one.

![image](https://user-images.githubusercontent.com/5660396/184058059-5d0b1601-ecdb-44af-a0d8-de48a0b5f3b9.png)

In the AutoResponder section, first enable rules and make sure unmatched requests passthrough is checked. Then click add rule and input `EXACT:https://images.neopets.com/games/g1347_v66_45083.swf` and then in the second box click the dropdown arrow and find file. Then browse your pc for the fixed swf file. You also need the shellconfig rule above

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

## Shockwave games

To play shockwave games you need to install it and use IE / chrome IE tab. If browser does not recognize you have the plugin already, you can add this rule:

```
if (oSession.uriContains("play_shockwave.phtml")) {
    var body = oSession.GetResponseBodyAsString();
    if (body.Contains("game_container")) {
        oSession.utilSetResponseBody(body.Replace('document.write', 'console.log').Replace("swRestart='false'", "swRestart='true'").Replace("swContextMenu='false'", "swContextMenu='true'"));
    }
}
```

Note that unlike the other rules it does not go in OnBeforeRequest section, it goes in the OnBeforeResponse.

![image](https://user-images.githubusercontent.com/5660396/184269837-e09895e8-da86-4df7-99a6-ac6dd04b7446.png)

When a game does not load/gets stuck at loading, right click on it and hit restart. As for hannah and the ice caves, if you get the "Sorry. It appears that this game is not running at its intended location" error, you need to hold shift + o + k while it loads for it to work. 

## Neohome v2

```
if (oSession.uriContains("neohome/property/")) {
    var body = oSession.GetResponseBodyAsString();
    if (body.Contains("NeoHomeApplication_v")) {
        oSession.utilSetResponseBody(body.Replace('services.neopets', 'www.neopets').Replace("http%3A", "https%3A"));
    }
}
```

Note that unlike the other rules it does not go in OnBeforeRequest section, it goes in the OnBeforeResponse

## Kacheek Seek

```
if (oSession.uriContains("process_hideandseek.phtml")) {
  oSession["Referrer"] = oSession["Referrer"].replace("https", "http");
}
```

This fixes being able to play kacheek seek

## With header editor (easiest setup but many games won't work)

1. Do Waterfox steps from [this reddit post](https://www.reddit.com/r/neopets/comments/s7jzyt/how_to_enable_flash_post_endoflife/)
2. Install [Header Editor](https://addons.mozilla.org/en-US/firefox/addon/header-editor/?utm_source=addons.mozilla.org&utm_medium=referral&utm_content=search)
3. Click extension icon -> manage -> Export and Import
4. Paste in Download Rule URL https://raw.githubusercontent.com/juvian/neopets-flash-fix/main/header-editor/rules.json
5. Click download icon and then click save
