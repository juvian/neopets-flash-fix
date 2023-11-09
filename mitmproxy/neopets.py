import os
import re
from pathlib import Path
from typing import Optional

from mitmproxy import ctx, http
from mitmproxy.addonmanager import Loader

saved_cookies: Optional[http.Headers] = None

FILES_DIR = str(Path(__file__).parent)

def load(loader: Loader) -> None:
    ctx.options.http2 = False

def request(flow: http.HTTPFlow) -> None:
    url = flow.request.pretty_url
    if "neopets.com" in flow.request.host:
        #fixes games pointing to dev server that have chinese lang when offline
        if "gettranslationxml.phtml" in url and flow.request.method == "POST" and "lang" in flow.request.urlencoded_form:
            flow.request.urlencoded_form["lang"] = "en"

def requestheaders(flow: http.HTTPFlow) -> None:
    global saved_cookies
    url = flow.request.pretty_url
    if "neopets.com" in flow.request.host or "virtools" in flow.request.host:
        flow.request.scheme = "https"
        flow.request.port = 443

        if flow.request.host == "dev.neopets.com":
            flow.request.host = "www.neopets.com"
            #try to fix cookies not sent to dev to bypass stackpath
            if saved_cookies:
                flow.request.headers["cookie"] = saved_cookies
        elif flow.request.host == "www.neopets.com":
            saved_cookies = flow.request.headers["cookie"]
        
        #fixes Clara on Ice, Let it Slide, Extreme Potato Counter
        if ".swf" in url or "/config.xml" in url or "/shellconfig.xml" in url:
            flow.request.host = "images.neopets.com"
            flow.request.url = re.sub(r"/games/.*/games/", "/games/", flow.request.url).replace("games/games", "games")
        
        #fixes 3dvia games like Terror Mountain Tilt
        if "virtools.download.akamai.com/6712/player/install/" in url:
            flow.request.url = "https://3dlifeplayer.dl.3dvia.com/" + url[url.rindex("player/install"):]
        
        #fixes kacheek seek
        if "process_hideandseek.phtml" in url:
            flow.request.headers["referer"] = "http://www.neopets.com/games/hidenseek"
        
        if url.endswith(".swf") or url.endswith(".txt"):
            p = flow.request.path.replace('/', os.sep)
            for path in [Path(FILES_DIR + p), Path(str(Path(__file__).resolve()).split("mitmproxy")[0] + "Fiddler" + os.sep + "neopets" + p)]:
                if path.is_file():
                    flow.response = http.Response.make(200, open(path, "rb").read())


def response(flow: http.HTTPFlow) -> None:
    url = flow.request.pretty_url
    if "neopets.com" in flow.request.host and flow.response is not None and flow.response.content is not None:
        #fixes shockwave games
        if "play_shockwave.phtml" in url and b"game_container" in flow.response.content:
            flow.response.content = flow.response.content.replace(b"document.write", b"console.log").replace(b"swRestart='false'", b"swRestart='true'").replace(b"swContextMenu='false'", b"swContextMenu='true'")

        #fixes neohome v2
        if "neohome/property/" in url:
            flow.response.content = flow.response.content.replace(b"services.neopets", b"www.neopets").replace(b"http%3A", b"https%3A")
