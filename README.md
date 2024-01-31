Another user has made a more [detailed guide](https://github.com/themrrobert/neopets-flash-fix-windows-10) for Windows you might want to check instead.

# How to play most games

You will need to setup Fiddler (Windows only) or mitmproxy (MacOS only). Waterfox browser 3.2.6 is recommended for most games.

### Shockwave
1. Follow [shockwave guide](https://www.youtube.com/watch?v=LdkiSc5TNL0). I don't think the IE tab option works

### 3dvia games

1. Follow [3dvia guide](https://www.youtube.com/watch?v=NH8WfY7MvU4)

When a game does not load/gets stuck at loading, right click on it and hit restart. As for hannah and the ice caves, if you get the "Sorry. It appears that this game is not running at its intended location" error, you need to hold shift + o + k while it loads for it to work. 

### Waterfox

1. Install a browser that supports Flash like Waterfox 3.2.6 (for [Windows](https://cdn.waterfox.net/releases/win64/installer/Waterfox%20G3.2.6%20Setup.exe) or [MacOS](https://cdn.waterfox.net/releases/osx64/installer/Waterfox%20G3.2.6%20Setup.dmg)).
2. Immediately open Waterfox after installation and go to about:preferences. Under Waterfox Updates, allow Waterfox to "Check for updates but let you choose to install them" instead of "Automatically install updates (recommended)".
3. Go to about:config and search for security.enterprise_roots.enabled, then double click it to change it to true.

### Flash Player

1. Install Flash 32.0.0.293 **while disconnected from the Internet**. Currently the Flash zip can be found [here](https://archive.org/details/flashplayerarchive). On the right, click "ZIP FILES" to expand it, and scroll down to find and download fp_32.0.0.293_archive.zip. Install it.
2. Set Flash to not automatically update at the end of the installation process, then you can reconnect to the Internet.

# Fiddler Setup (Windows)

1. Install [Fiddler Classic](https://www.telerik.com/download/fiddler)
2. Find fiddler script folder (usually Documents\Fiddler2\Scripts) and replace/add [CustomRules.js](/fiddler/CustomRules.js). Another option is in fiddler go to rules -> customize rules and overwrite the content with my file. 
3. In fiddler go to Tools -> Options -> HTTPS -> make sure capture https connect, decrypt https traffic and ignore server certificate errors are enabled. Restart fiddler 
4. Open fiddler
5. Go to https://images.neopets.com and accept risks if it prompts you about it
5. Play

### Extra

Some swf games like [Assignment 53](https://www.neopets.com/games/game.phtml/?game_id=1347&size=regular&quality=high&play=true) and [Coal Wars](https://www.neopets.com/games/game.phtml?game_id=1370&size=regular&quality=high&play=true) require manual fixing to be able to send scores, as some newer games think they are not running in production now with https. Some txt files also require manual loading in order to not get hit by stackpath while playing like Edna's shadow, Crisis courier and Stowaway Sting.

1. Download [neopets folder](https://download-directory.github.io/?url=https://github.com/juvian/neopets-flash-fix/tree/main/neopets)
2. Find fiddler installation path (usually C:\Program Files\Fiddler), create a neopets folder and unzip files inside it. Should end up looking like neopets/games/...

# Mitmproxy Setup (MacOS)
1. In Waterfox, again go to about:preferences and search for proxy. Click on settings and Select Manual proxy configuration, then set HTTP Proxy to 127.0.0.1 with port 8080. Make sure to also check the box to "Also use this proxy for FTP and HTTPS". [IE has a similar setup](https://docs.microsoft.com/en-us/troubleshoot/developer/browsers/connectivity-navigation/use-proxy-servers-with-ie)

![image](https://user-images.githubusercontent.com/5660396/185045695-d6c32114-e096-4533-8e16-1e0eaaadfa66.png)

2. Install [Mitmproxy](https://mitmproxy.org/). The easiest way is via [Homebrew](https://brew.sh/) on the MacOS Terminal:
```
brew install mitmproxy
```
3. Create a [neopets.py](/mitmproxy/neopets.py) file. The location does not matter, but as an example, the following command takes you to your home directory and creates a new directory called neopets:
```
cd ~
mkdir neopets
```
Then, the following command opens a new file, and copies and pastes the content from [neopets.py](/mitmproxy/neopets.py):
```
vim neopets/neopets.py
(press i)
(ensure that you have all the lines of that file in your clipboard, then press cmd+v)
(press :wq, as in colon, w, q)
```
(You can substitute vim with your favorite text editor, or use Sublime Text, etc. As long as you save that content in a file somewhere for the next step.)

4. Now run mitmdump with that new file as the script (-s):
```
mitmdump -s ./neopets/neopets.py
```
This launches mitmproxy using our specified configuration. **You will run this command every time you want to play Flash games.**

*(Pressing ctrl+c on the terminal window you ran mitmproxy from will stop the program running once you're done. Closing the terminal or rebooting will also stop it.)*

5. In Waterfox, while mitmproxy is running, go to http://mitm.it/ and go to the MacOS line. Download the mitmproxy-ca-cert.pem file (in the example below, it was placed in ~/Downloads). Click Show instructions and note the command for "Automated installation". Open a new Terminal window (since currently we're running mitmproxy in our first one) and run that command in the terminal; enter your password when prompted to allow it:
```
sudo security add-trusted-cert -d -p ssl -p basic -k /Library/Keychains/System.keychain ~/Downloads/mitmproxy-ca-cert.pem
```

6. You must wait for the certificate to take effect. As long as you are still seeing "This certificate is marked as not trusted for all users" when examining that certificate in the Keychain Access tool (you can open Keychain Access and search for mitmproxy to find it), it will cause the sites you visit to throw certificate errors. After about 10-15 minutes it should switch over to "This certificate is marked as trusted for all users." 

If any issues, verify that if you double-click that certificate in Keychain Access and click to expand the "Trust" category, your working configuration has Secure Sockets Layer (SSL) set to Always Trust, and X.509 Basic Policy to Always Trust, with the other values left unspecified, and it should say "This certificate is marked as trusted for all users." at the top.

7. Try playing any Flash game in Neopets. Make sure mitmproxy has been launched. You might have to allow keyboard access to Waterfox: Go to System Preferences > Privacy & Security > Privacy Tab at the top > Find Input Monitoring (64-bit systems // Catalina and later) on the right > click the lock in bottom left & input password > add WaterFox.

### Extra

1. Download [neopets folder](https://download-directory.github.io/?url=https://github.com/juvian/neopets-flash-fix/tree/main/neopets)
2. Find mitmproxy installation path, go to mitmproxy/addons/neopets folder and unzip games folder there. Directory should end up with neopets.py file and games folder

# Troubleshooting 
1. If using waterfox, make sure it says version G3.2.6 when going to about:support
2. Go to about:preferences in waterfox, search for proxy and click settings. If using fiddler, make sure Use System Proxy is checked. If using mitmproxy, make sure Manual proxy configuration is checked
3. Make sure to accept risk and continue with [neopets images](https://images.neopets.com/) if asked
4. If you go to about:plugins in waterfox, make sure flash version is 32.0.0.371 or lower
5. If Assignment 53 is still not working after having completed extra steps, try opening developer console in waterfox (ctrl + shift + i), then go to network tab, check disable cache and then refresh game page
6. If you send a score and it gets blocked by stackpath, you can go to fiddler log tab, scroll to bottom and see the url that was sent to process the score. Copy it and open it manually in a new tab and it should send. 
![image](https://user-images.githubusercontent.com/5660396/210623327-1adcdbbc-e998-49b4-b5b3-a026feef87d2.png)
7. If 3dvia games are the ones not working, go [here](https://3dlifeplayer.dl.3dvia.com/player/install/3DLifePlayer.js) and accept risk if prompted

# Can't login to IE
A more technical way of logging in is to login in your usual browser like chrome, open developer console (ctrl + shift + i), write `document.cookie.split(';').find(c => c.includes('neologin')).trim()` in console, hit enter and you will see something like neologin=youruserxxxxx (don't show anyone this value!!!).
Then in Ie visit neopets.com, open developer console (f12) and write `document.cookie = "yyy"` where yyy is what you got from chrome (neologin=youruserxxxxx). Then refresh and you should be logged in.

# Header editor setup (easiest setup but many games won't work)

1. Install [Header Editor](https://addons.mozilla.org/en-US/firefox/addon/header-editor/?utm_source=addons.mozilla.org&utm_medium=referral&utm_content=search)
2. Click extension icon -> manage -> Export and Import
3. Paste in Download Rule URL https://raw.githubusercontent.com/juvian/neopets-flash-fix/main/header-editor/rules.json
4. Click download icon and then click save
