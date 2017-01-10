import urlparse
import requests
from requests.auth import HTTPBasicAuth


class Wick:
    def __init__(self, url=None):
        self.url = url
        self.response = None
        self.username = None
        self.password = None

    # http authentication
    def login(self, username, password):
        self.username = username
        self.password = password

    # set the url
    def set(self, url):
        if not url.startswith("http://") and \
        not url.startswith("https://"):
            url = "http://" + url
        self.url = url

    # download the webpage
    def get(self):
        response = None
        self.response = requests.get(self.url)

    # returns the downloaded webpage
    def payload(self):
        return self.response

    def pwd(self):
        return self.url

    # gets all links on webpage (including out of domain links)
    def ls(self):
        import urllib
        import lxml.html
        connection = urllib.urlopen(self.url)

        dom = lxml.html.fromstring(connection.read())

        # select the url in href for all a tags(links)
        for link in dom.xpath('//a/@href'):
            print link

    def rm(self, theData):
        theUrl = self.url
        return requests.delete(theUrl,
                               auth=HTTPBasicAuth(
                               self.username,
                               self.password))

    # copies a local or remote file to the server
    def cp(self, theData):
        if (theData.startswith('http://') or
        theData.startswith('https://')) and
        "\n" not in theData:
            theData = requests.get(theData)

        return requests.put(self.url, data=theData)

    def cd(self, cdLocation):
        url = None
        cdLocation = cdLocation.strip()
        if cdLocation == "..":
            url = '/'.join(self.url.split("/")[:-1])
            print url
        else:
            if "." in cdLocation:
                url = urlparse.urljoin(self.url + "/", cdLocation)
            else:
                url = urlparse.urljoin(self.url, cdLocation)

                self.url = url
        return url
