from mitmproxy import ctx, http
from pathlib import Path

saved_cookies = None

FILES_DIR = str(Path(__file__).parent)

def load(loader):
    ctx.options.http2 = False

def request(flow):
    url = flow.request.pretty_url
    if "neopets.com" in flow.request.host:
        #fixes games pointing to dev server that have chinese lang when offline
        if "gettranslationxml.phtml" in url and flow.request.method == "POST" and "lang" in flow.request.urlencoded_form:
            flow.request.urlencoded_form["lang"] = "en"

def requestheaders(flow):
    global saved_cookies
    url = flow.request.pretty_url
    if "neopets.com" in flow.request.host:
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
            flow.request.url = flow.request.url.replace("/games/https://images.neopets.com/games/", "/games/").replace("games/games", "games")
        
        #fixes 3dvia games like Terror Mountain Tilt
        if "virtools.download.akamai.com/6712/player/install/" in url:
            flow.request.url = "https://3dlifeplayer.dl.3dvia.com/" + url.substring(url.lastIndexOf("player/install"))
        
        #fixes kacheek seek
        if "process_hideandseek.phtml" in url:
            flow.request.headers["referer"] = "http://www.neopets.com/games/hidenseek"
        
        if url.endswith(".swf") or url.endswith(".txt"):
            path = Path(FILES_DIR + flow.request.path.replace('/', '\\'))
            if path.is_file():
                flow.response = http.Response.make(200, open(path, "rb").read())


def response(flow):
    url = flow.request.pretty_url
    if "neopets.com" in flow.request.host:
        #fixes shockwave games
        if "play_shockwave.phtml" in url and "game_container" in flow.response.content:
            flow.response.content = flow.response.content.replace(b"document.write", b"console.log").replace(b"swRestart='false'", b"swRestart='true'").replace(b"swContextMenu='false'", b"swContextMenu='true'")

        #fixes neohome v2
        if "neohome/property/" in url:
            flow.response.content = flow.response.content.replace(b"services.neopets", b"www.neopets").replace(b"http%3A", b"https%3A")
