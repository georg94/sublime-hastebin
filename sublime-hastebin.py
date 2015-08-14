import sublime, sublime_plugin
import json
import webbrowser
# import urllib
try:
  import urllib2 as urllib
except ImportError:
  import urllib.request as urllib
# import urljoin
try:
  from urlparse import urljoin
except (ImportError) as e:
  from urllib.parse import urljoin

class UploadToHastebin( sublime_plugin.TextCommand ):
  def run(self, view):
    # load settings
    settings = sublime.load_settings("sublime-hastebin.sublime-settings")

    # and get hastebin URL
    hastebinUrl = settings.get("hastebin-url")

    # if the user only enters a hostname without "http[s]://" I'll add "http://" for him
    if not (hastebinUrl.startswith("http://") or hastebinUrl.startswith("https://")):
      hastebinUrl = "http://" + hastebinUrl

    # if the user only entered the url to hastebin without "documents" that will be fixed
    # tbh I also leave "documets" away in the config
    if not "document" in hastebinUrl:
      hastebinUrl = urljoin(hastebinUrl, "documents")

    # check if something is selected

    document = ""
    for region in self.view.sel():
      if not region.empty():
        # there is a selection, only upload that
        document += "\n" + str(self.view.substr(region))
      else:
        # no selection -> uplaod the whole document
        document = self.view.substr(sublime.Region(0, self.view.size()))

    document = document.encode("utf8")

    # now do the upload
    request = urllib.Request(hastebinUrl, document)
    response = urllib.urlopen(request)
    body = response.read()

    # get key from answer body
    documentKey = json.loads(body.decode("utf8"))["key"]

    # see if the current file has a extension, if yes append it to the key.
    # That will make hastebin highlight it in the right syntax.
    window = self.view.window()
    if "file_extension" in window.extract_variables():
      documentKey += "."+window.extract_variables()["file_extension"]
    url = urljoin(hastebinUrl, documentKey)

    # copy to clipboard if enabled
    if settings.get("copy-to-clipboard"):
      sublime.set_clipboard(url)
    # open in browser if enabled
    if settings.get("open-in-browser"):
      webbrowser.open_new_tab(url)