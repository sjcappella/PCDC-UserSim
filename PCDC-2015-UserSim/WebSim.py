__author__ = 'Sam Cappella'

import os
import getpass
import socket
import threading
import urllib2

from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Global variables
"""
Putting variables here for time related events was a design choice to make it easier to view and modify based on
the pace of the competition. This is not the most Pythonic way to do this, but the code works and it is easy. This
also makes it easier to debug because you can simply edit the value of the global variable to shorten long events.
"""
browse = True                   # Global variable of browsing
dispatchLowBound = 15           # Lower bound of time to dispatch event in seconds
dispatchUpperBound = 300        # Upper bound of time to dispatch event in seconds
timingPause = 2                 # A timing pause in seconds to keep things smooth
browseTime = 30                 # Production time to browse a web page in seconds
#browseTime = 2                 # Debug time to browse a web page in seconds
pageTimeOut = 45                # Time to wait for a web page timeout in seconds
implicitWait = 15               # Some pages may load with broken parts causing browser get to block, but we are ok
eventPause = 3                  # Number of seconds to wait in between each event
writeGoogleQuery = 5            # Number of seconds to type a Google query
viewGoogleQuery = 10            # Number of seconds to view a Google query result
watchFullYoutubeVideo = True    # Boolean to watch the full YouTube videos
youtubeVideoWatchDebug = 15     # Number of seconds to watch a YouTube video in debug
wikiSpiderDepth = 10            # Number of random links to follow on Wikipedia
firefoxProfilePath = ""         # Path to the Firefox Profile

# Define web simulator class
class WebSim(threading.Thread):

    # Default constructor
    def __init__(self, logger, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)
        self.logger = logger
        self.args = args
        self.kwargs = kwargs
        self.logger.log("Web Simulation created.")

        # Setup Firefox Profile
        global firefoxProfilePath
        path = "C:\\Users\\" + getpass.getuser() + "\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\"
        files = os.listdir(path)
        profilePath = ""
        for file in files:
            if file[-8:] == ".default":
                firefoxProfilePath = path + file
                self.logger.log("Found default Firefox profile: " + firefoxProfilePath)

    # Define run function
    def run(self):
        self.logger.log("Web simulation running...")

        # Reset browse global boolean
        global browse
        browse = True

        # Create dispatch table
        dispatch = {
            1 : self.browseGreatestHits,
            2 : self.browseGreatestHits,
            3 : self.browseRandomXkcd,
            4 : self.googleSearch,
            5 : self.youtubeVideo,
            6 : self.crawlWikipedia,
            7 : self.browseCompanySite,
        }

        # Count the number of web events, and pick a random int corresponding to one, then dispatch the function
        numEvents = len(dispatch)
        # Main browse event loop
        while browse:
            functionIndex = randint(1, numEvents)
            dispatch[functionIndex]()
            sleep(eventPause)

    # Function to stop browsing
    def stop(self):
        global browse
        browse = False

    # Function to score the web traffic simulator
    def score(self):
        try:
            self.logger.log("Scoring Web Simulator activity.")
            # Open browser to the scoring page
            browser = webdriver.Firefox(webdriver.FirefoxProfile(firefoxProfilePath))
            browser.get("http://x.x.x.x/score-bot-page")
            source = browser.page_source
            browser.quit()
            if "score-bot-traffic-nothing-to-see-here" in source:
                return True
            else:
                return False
        except Exception as e:
            self.logger.log("Error scoring Web Simulator activity.")
            self.logger.log(str(e))
            return False
            try:
                browser.quit()
            except:
                pass

    # Function to browse company website
    def browseCompanySite(self):
        blue = ""
        ipAddress = socket.gethostbyname(socket.gethostname())
        if ipAddress == "127.0.0.1":
            return

        octets = ipAddress.split('.')
        blue = ""
        if octets[2] == "10":
            blue = "blue1"
        elif octets[2] == "20":
            blue = "blue2"
        elif octets[2] == "30":
            blue = "blue3"
        elif octets[2] == "40":
            blue = "blue4"
        elif octets[2] == "50":
            blue = "blue5"
        elif octets[2] == "60":
            blue = "blue6"
        elif octets[2] == "70":
            blue = "blue7"
        elif octets[2] == "80":
            blue = "blue8"
        else:
            return
        webAddress = "duke." + blue + ".pcdc"
        # Handle generic error
        try:
            browser = webdriver.Ie()
            # Wait for the page to load, then quit if it doesn't
            browser.set_page_load_timeout(pageTimeOut)
            # Handle error if page takes too long to load
            try:
                browser.get("http://" + webAddress)
                sleep(browseTime)
            except:
                self.logger.log("Page took too long to load.")
            browser.quit()
        except Exception as e:
            self.logger.log("Error browsing internal web sites.")
            self.logger.log(str(e))
            try:
                browser.quit()
            except:
                pass

    # Function to browse the most popular websites
    # Modified to work with the 2015 PCDC whitelist
    def browseGreatestHits(self):
        # Define the sites to randomly browse
        sites = {
            1 : "http://www.google.com",
            2 : "http://www.about.com",
            3 : "http://www.youtube.com",
            4 : "http://www.yahoo.com",
            5 : "http://www.amazonaws.com",
            6 : "http://www.wikipedia.org",
            7 : "http://www.apache.com",
            8 : "http://www.cert.org",
            9 : "http://www.centos.org",
            10 : "http://www.bing.com",
            11 : "http://www.ask.com",
            12 : "http://www.cisco.com",
            13 : "http://www.debian.org",
            14 : "http://www.thegeekstuff.com",
            15 : "http://www.wikihow.com",
            16 : "http://www.sans.org",
            17 : "http://www.redhat.com",
            18 : "http://www.python.org",
            19 : "http://www.owasp.org",
            20 : "http://www.microsoft.com",
            21 : "http://www.stackoverflow.com",
            22 : "http://www.lifehacker.com",
            23 : "http://www.java.com",
            24 : "http://www.gnu.org",
            25 : "http://www.linuxquestions.org",
            26 : "http://www.mozilla.org",
            27 : "http://www.nmap.org",
            28 : "http://www.nationalccdc.org",
            29 : "http://www.pcdc-sc.com",
            30 : "http://twitter.com/palmettocyber",
        }

        # Randomly pick a site to browse
        numSites = len(sites)
        siteIndex = randint(1, numSites)
        # Handle generic error
        try:
            browser = webdriver.Ie()
            # Wait for the page to load, then quit if it doesn't
            browser.set_page_load_timeout(pageTimeOut)
            # Handle error if page takes too long to load
            try:
                browser.get(sites[siteIndex])
                sleep(browseTime)
            except:
                self.logger.log("Page took too long to load.")
            browser.quit()
        except Exception as e:
            self.logger.log("Error browsing most popular web sites.")
            self.logger.log(str(e))
            try:
                browser.quit()
            except:
                pass

    # Function to go to a random XKCD comic
    def browseRandomXkcd(self):
        # Handle generic error
        try:
            browser = webdriver.Ie()
            browser.set_page_load_timeout(pageTimeOut) # On some networks XKCD pictures don't load, set timeout just in case
            browser.get("http://c.xkcd.com/random/comic/")
            sleep(browseTime)
            browser.quit()
        except:
            self.logger.log("Error laughing at XKCD.")
            self.logger.log(str(e))
            try:
                browser.quit()
            except:
                pass

    # Function to perform Google search
    def googleSearch(self):
        # Terms to search google for
        queries = {
            1 : "what is an esxi",
            2 : "how much wood would a wood-chuck chuck if a wood-chuck could chuck wood?",
            3 : "42",
            4 : "do a barrel roll",
            5 : "recursion",
            6 : "number of horns on a unicorn",
            7 : "how big are velociraptors?",
            8 : "how to tell if you've been hacked",
            9 : "what is ssh",
            10 : "palmetto cyber defense competition",
        }

        # Pick random query
        numQueries = len(queries)
        queryIndex = randint(1, numQueries)
        # Handle generic error
        try:
            # Open up Google homepage
            browser = webdriver.Ie()
            browser.get("http://www.google.com")
            assert "Google" in browser.title
            # Find the search box, type in query, and hit enter
            element = browser.find_element_by_name("q")
            element.send_keys(queries[queryIndex])
            sleep(writeGoogleQuery)
            element.send_keys(Keys.RETURN)
            sleep(viewGoogleQuery)
            browser.quit()
        except Exception as e:
            self.logger.log("Error searching Google.")
            self.logger.log(str(e))
            try:
                browser.quit()
            except:
                pass

    # Function to watch youtube videos
    def youtubeVideo(self):
        """
         Dictionary of youtube video info
         <index> : ("<youtube search term>", "<video extension>", <length of video in seconds>)
         The dictionary is a map from indices to a tuple of the youtube search terms, the video extension, and the
         length of the video in seconds. This lets the youtube browsing be sightly more realistic because the
         simulator will search for a video using the search term. But, the user will then just select the video based
         on the actual extension. Eg: https://www.youtube.com/watch?v=QH2-TGUlwu4 where <QH2-TGUlwu4> is the extension.

         Also, because of YouTube's lack of support for IE8, we will use FireFox to keep everything running smooth.
        """
        # List of search tearms, URL extensions, and running time in seconds of YouTube videos
        youtubeVideos = {
            1 : ("nyan cat", "QH2-TGUlwu4", 217),
            2 : ("palmetto cyber defense competition", "CbrtF_Gbeyc", 76),
            3 : ("tracert next gen hacker", "SXmv8quf_xM", 268),
            4 : ("how do i track a killer in real time with visual basic gui", "hkDD03yeLnU", 17),
            5 : ("double hacking to better protect the firewall", "1Y2zo0JN2HE", 90),
        }

        # Pick a random video
        numVideos = len(youtubeVideos)
        videoIndex = randint(1, numVideos)
        # Handle generic errors
        try:
            # Open up YouTube main page in Firefox
            browser = webdriver.Firefox(webdriver.FirefoxProfile(firefoxProfilePath))
            browser.get("https://www.youtube.com/")
            assert "YouTube" in browser.title
            # Find the search box, type in the video search term, and hit enter
            element = browser.find_element_by_name("search_query")
            element.send_keys(youtubeVideos[videoIndex][0])
            sleep(timingPause)
            element.send_keys(Keys.RETURN)
            sleep(timingPause)
            # Actually browse directly to the video's URL
            browser.get("https://www.youtube.com/watch?v=" + youtubeVideos[videoIndex][1])
            if watchFullYoutubeVideo is True:
                sleep(youtubeVideos[videoIndex][2])
            else:
                sleep(youtubeVideoWatchDebug)
            browser.quit()
        except Exception as e:
            self.logger.log("Error watching YouTube videos.")
            self.logger.log(str(e))
            try:
                browser.quit()
            except:
                pass

    # Function to crawl Wikipedia
    def crawlWikipedia(self):
        # Track if a picture was downloaded
        pictureDownloaded = False
        # A list of first pages to search for
        firstPages = {
            1 : "linux",
            2 : "freebsd",
            3 : "mac os x",
            4 : "microsoft windows",
            5 : "plan 9 from bell labs",
            6 : "minix",
            7 : "beos",
            8 : "debian linux",
            9 : "unix",
        }

        # Pick a random page
        numPages = len(firstPages)
        pageIndex = randint(1, numPages)

        # Handle generic error
        try:
            # Open up Internet Explorer and browse to Wikipedia homepage
            browser = webdriver.Ie()
            browser.get("http://www.wikipedia.org")
            # Find the search box, type in the search term, and hit enter
            element = browser.find_element_by_id("searchInput")
            element.send_keys(firstPages[pageIndex])
            sleep(timingPause)
            element.send_keys(Keys.RETURN)
            sleep(timingPause)
            i = 0
            pictureDepth = randint(0, wikiSpiderDepth-2)
            # Loop to spider Wikipedia a number of times
            while i is not wikiSpiderDepth:
                # Check to see if an attempt to download a picture should be made and make it on a random page
                if pictureDownloaded is False and i >= pictureDepth:
                    pictureElements = browser.find_elements_by_tag_name("img")
                    pictureDownloaded = self.savePicture(pictureElements)

                # Find all hyper link elements in a page
                elements = browser.find_elements_by_tag_name('a')
                links = []

                # Isolate 'href' tags and get the contents
                for element in elements:
                    link = element.get_attribute('href')
                    # Ensure link exists
                    if link is None:
                        continue
                    # Make sure link points to Wikipedia
                    elif "http://en.wikipedia.org/wiki/" in link:
                        # Exclude Wikipedia citation links in an article
                        if "cite_note" in link:
                            continue
                        # Exclude Wikipedia reference links in an article
                        if "cite_ref" in link:
                            continue
                        # Link has pass all our criteria, add it to the list
                        else:
                            links.append(link)
                    else:
                        continue
                # Make sure links were actually found
                if len(links) is not 0:
                    # If more than 1 link was found, randomly pick one, otherwise, just use the only link found
                    maxLinks = len(links)
                    if maxLinks is not 1:
                        linkIndex = randint(1, maxLinks - 1)
                    else:
                        linkIndex = 1
                    # Go to new link
                    self.logger.log("Going to: " + links[linkIndex])
                    browser.get(links[linkIndex])
                    sleep(browseTime)
                    i += 1
                else:
                    break

            browser.quit()
        except Exception as e:
            self.logger.log("Error spidering Wikipedia.")
            self.logger.log(str(e))
            try:
                browser.quit()
            except:
                pass

    # Define function to determine if link is a picture
    def savePicture(self, pictureElement):
        try:
            pictures = []
            for picture in pictureElement:
                pictureLink = picture.get_attribute("src")
                if pictureLink is not None:
                    pictures.append(pictureLink)
            # Pick a random picture, usually don't want it to be the first one (index = 0)
            numLinks = len(pictures)
            if numLinks is 0:
                return False
            if numLinks > 1:
                pictureIndex = randint(1, numLinks - 1)
            else:
                pictureIndex = 1

            self.logger.log("Saving the following picture: " + pictures[pictureIndex])
            url = pictures[pictureIndex]
            userName = getpass.getuser()
            dirPath = "C:\\Users\\" + userName + "\\SimResources\\Uploads\\"
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)

            # Check to make sure file doesn't already exist first
            fileName = url.split('/')[-1]
            fileName = dirPath + fileName
            self.logger.log("Saving file as: " + fileName)
            download = urllib2.urlopen(url)
            file = open(fileName, 'wb')
            file.write(download.read())
            file.close()
            return True
        except Exception as e:
            self.logger.log("Error saving file.")
            self.logger.log(str(e))

