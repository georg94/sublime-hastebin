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
    settings = sublime.load_settings("sublime-hastebin.sublime-settings")
    hastebinUrl = settings.get("hastebin-url")
    if not (hastebinUrl.startswith("http://") or hastebinUrl.startswith("https://")):
      hastebinUrl = "http://" + hastebinUrl
    if not "document" in hastebinUrl:
      hastebinUrl = urljoin(hastebinUrl, "documents")

    for region in self.view.sel():
      if not region.empty():
        document = self.view.substr(region).encode("utf8")
      else:
        document = self.view.substr(sublime.Region(0, self.view.size())).encode("utf8")

      request = urllib.Request(hastebinUrl, document)
      response = urllib.urlopen(request)
      body = response.read()

      documentKey = json.loads(body.decode("utf8"))["key"]

      window = self.view.window()
      if "file_extension" in window.extract_variables():
        documentKey += "."+window.extract_variables()["file_extension"]
      url = urljoin(hastebinUrl, documentKey)

      if settings.get("copy-to-clipboard"):
        sublime.set_clipboard(url)
      if settings.get("open-in-browser"):
        webbrowser.open_new_tab(url)