# How to play most flash games

## With Fiddler

1. Do Waterfox steps from [this reddit post](https://www.reddit.com/r/neopets/comments/s7jzyt/how_to_enable_flash_post_endoflife/)
2. Install [Fiddler Classic](https://www.telerik.com/download/fiddler) (if mac, try [virtual machine] or do the with mitmproxy steps)
3. Find fiddler script folder (usually Documents\Fiddler2\Scripts) and replace [CustomRules.js](/fiddler/CustomRules.js)
4. Open fiddler
5. Play

### Extra

Some swf games like [Assignment 53](https://www.neopets.com/games/game.phtml/?game_id=1347&size=regular&quality=high&play=true) and [Coal Wars](https://www.neopets.com/games/game.phtml?game_id=1370&size=regular&quality=high&play=true) require manual fixing to be able to send scores, as some newer games think they are not running in production now with https. Some txt files also require manual loading in order to not get hit by stackpath while playing like Edna's shadow, Crisis courier and Stowaway Sting.

1. Download [neopets folder](https://download-directory.github.io/?url=https://github.com/juvian/neopets-flash-fix/tree/main/neopets)
2. Find fiddler installation path (usually C:\Program Files\Fiddler), create a neopets folder and unzip files inside it. Should end up looking like neopets/games/...

## With Mitmproxy
1. Install Waterfox from [this reddit post](https://www.reddit.com/r/neopets/comments/s7jzyt/how_to_enable_flash_post_endoflife/) if you want to play use flash. For shickwave/3dvia just need IE or chrome + IE tab
2. In waterfox go to about:config then search security.enterprise_roots.enabled and change it to true
3. In waterfox go to about:preferences then search for proxy then click on settings and Set Manual proxy configuration to 127.0.0.1 with port 8080. Make sure to also check use this proxy for FTP and HTTPs

![image](https://user-images.githubusercontent.com/5660396/185045695-d6c32114-e096-4533-8e16-1e0eaaadfa66.png)

4. Install [Mitmproxy](https://mitmproxy.org/)
5. Find mitmproxy installation path, go to mitmproxy/addons folder, create a neopets folder and put the [neopets.py](/mitmproxy/neopets.py) file inside it (something like C:\Program Files\mitmproxy\bin\mitmproxy\addons\neopets)
6. Find mitmproxy installation path, create a shortcut out of mitmdump.exe. Right click shortcut -> properties -> add -s mitmproxy\addons\neopets\neopets.py to the end of target (should end up like "C:\Program Files\mitmproxy\bin\mitmdump.exe" -s mitmproxy\addons\neopets\neopets.py). Click apply
7. Run mitmproxy (double click shortcut)
8. Go to [http://mitm.it/](http://mitm.it/). Show instructions and install certificate 
9. Play

### Extra

1. Download [neopets folder](https://download-directory.github.io/?url=https://github.com/juvian/neopets-flash-fix/tree/main/neopets)
2. Find mitmproxy installation path, go to mitmproxy/addons/neopets folder and unzip games folder there. Directory should end up with neopets.py file and games folder

## With header editor (easiest setup but many games won't work)

1. Do Waterfox steps from [this reddit post](https://www.reddit.com/r/neopets/comments/s7jzyt/how_to_enable_flash_post_endoflife/)
2. Install [Header Editor](https://addons.mozilla.org/en-US/firefox/addon/header-editor/?utm_source=addons.mozilla.org&utm_medium=referral&utm_content=search)
3. Click extension icon -> manage -> Export and Import
4. Paste in Download Rule URL https://raw.githubusercontent.com/juvian/neopets-flash-fix/main/header-editor/rules.json
5. Click download icon and then click save
