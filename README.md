# How to play most games

You will need to setup fiddler (windows only) or mitmproxy (should just use if mac as fiddler is easier). Depending on the type of games you want to play you might require IE / chrome with IE tab or waterfox browser

### Shockwave
1. Follow [shockwave guide](https://www.youtube.com/watch?v=LdkiSc5TNL0)

### 3dvia games

1. Follow [3dvia guide](https://www.youtube.com/watch?v=NH8WfY7MvU4)

When a game does not load/gets stuck at loading, right click on it and hit restart. As for hannah and the ice caves, if you get the "Sorry. It appears that this game is not running at its intended location" error, you need to hold shift + o + k while it loads for it to work.

### Flash games

1. Install a browser that supports flash like [waterfox](https://cdn.waterfox.net/releases/win64/installer/Waterfox%20G3.2.6%20Setup.exe) and [flash](http://andkon.com/arcade/faq.php). For other options check [this reddit post](https://www.reddit.com/r/neopets/comments/s7jzyt/how_to_enable_flash_post_endoflife/).
2. In waterfox go to about:config then search security.enterprise_roots.enabled and change it to true

# Fiddler Setup (Windows)

1. Install [Fiddler Classic](https://www.telerik.com/download/fiddler) (if mac, try [virtual machine] or do the with mitmproxy steps)
2. Find fiddler script folder (usually Documents\Fiddler2\Scripts) and replace/add [CustomRules.js](/fiddler/CustomRules.js). Another option is in fiddler go to rules -> customize rules and overwrite the content with my file. 
3. In fiddler go to Tools -> Options -> HTTPS -> make sure capture https connect, decrypt https traffic and ignore server certificate errors are enabled. Restart fiddler 
4. Open fiddler
5. Go to https://images.neopets.com and accept risks if it prompts you about it
5. Play

### Extra

Some swf games like [Assignment 53](https://www.neopets.com/games/game.phtml/?game_id=1347&size=regular&quality=high&play=true) and [Coal Wars](https://www.neopets.com/games/game.phtml?game_id=1370&size=regular&quality=high&play=true) require manual fixing to be able to send scores, as some newer games think they are not running in production now with https. Some txt files also require manual loading in order to not get hit by stackpath while playing like Edna's shadow, Crisis courier and Stowaway Sting.

1. Download [neopets folder](https://download-directory.github.io/?url=https://github.com/juvian/neopets-flash-fix/tree/main/neopets)
2. Find fiddler installation path (usually C:\Program Files\Fiddler), create a neopets folder and unzip files inside it. Should end up looking like neopets/games/...

# Mitmproxy Setup (Mac)
1. In waterfox go to about:preferences then search for proxy then click on settings and Set Manual proxy configuration to 127.0.0.1 with port 8080. Make sure to also check use this proxy for FTP and HTTPs. [IE has a similar setup](https://docs.microsoft.com/en-us/troubleshoot/developer/browsers/connectivity-navigation/use-proxy-servers-with-ie)

![image](https://user-images.githubusercontent.com/5660396/185045695-d6c32114-e096-4533-8e16-1e0eaaadfa66.png)

2. Install [Mitmproxy](https://mitmproxy.org/)
3. Find mitmproxy installation path, go to mitmproxy/addons folder, create a neopets folder and put the [neopets.py](/mitmproxy/neopets.py) file inside it (something like C:\Program Files\mitmproxy\bin\mitmproxy\addons\neopets)
4. Find mitmproxy installation path, create a shortcut out of mitmdump.exe. Right click shortcut -> properties -> add -s mitmproxy\addons\neopets\neopets.py to the end of target (should end up like "C:\Program Files\mitmproxy\bin\mitmdump.exe" -s mitmproxy\addons\neopets\neopets.py). Click apply
5. Run mitmproxy (double click shortcut)
6. Go to [http://mitm.it/](http://mitm.it/). Show instructions and install certificate 
7. Play

### Extra

1. Download [neopets folder](https://download-directory.github.io/?url=https://github.com/juvian/neopets-flash-fix/tree/main/neopets)
2. Find mitmproxy installation path, go to mitmproxy/addons/neopets folder and unzip games folder there. Directory should end up with neopets.py file and games folder

# Troubleshooting 
1. If using waterfox, make sure it says version G3.2.6 when going to about:support
2. Go to about:preferences in waterfox, search for proxy and click settings. If using fiddler, make sure Use System Proxy is checked. If using mitmproxy, make sure Manual proxy configuration is checked
3. Make sure to accept risk and continue with [neopets images](https://images.neopets.com/) if asked
4. If you go to about:plugins in waterfox, make sure flash version is 32.0.0.371 or lower
5. If Assignment 53 is still not working after having completed extra steps, try opening developer console in waterfox (ctrl + shift + i), then go to network tab, check disable cache and then refresh game page
6. If you send a score and it gets blocked by stackpath, you can go to fiddler log tab and see the url that was sent to process the score. Copy it and open it manually in a new tab and it should send.

# Header editor setup (easiest setup but many games won't work)

1. Install [Header Editor](https://addons.mozilla.org/en-US/firefox/addon/header-editor/?utm_source=addons.mozilla.org&utm_medium=referral&utm_content=search)
2. Click extension icon -> manage -> Export and Import
3. Paste in Download Rule URL https://raw.githubusercontent.com/juvian/neopets-flash-fix/main/header-editor/rules.json
4. Click download icon and then click save
