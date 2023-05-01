import pyppeteer as pt
import asyncio
from pyppeteer.page import Page
from urllib.parse import urlparse
from bs4 import BeautifulSoup

Url = "https://www.concordia.ca/ginacody.html"

class Crawler:    
    def __init__(self, startUrl: str, limit: int):
        self.visited = []
        self.limit = limit
        self.id = 0
        self.startUrl = startUrl
        self.blacklist = [
            '[document]',
            'noscript',
            'header',
            'html',
            'meta',
            'head', 
            'input',
            'script',
            'style',
            'a',
        ]
    
    async def crawl(self, page: Page, link: str):
        try:         
            if (link.startswith('javascript')):
                return
            
            urlParse = urlparse(link)
            
            if (urlParse.netloc != "www.concordia.ca"):
                return
            
            parsedLink = urlParse.scheme + "://" + urlParse.netloc + urlParse.path
            self.visited.append(parsedLink)

            
            response = await page.goto(parsedLink)
            
            if (response.headers.get('content-type') != 'text/html'):
                return
            
            print("current page: " + parsedLink + ", id: " + str(self.id))
            
            await page.waitFor(200)
            
            await self.extractText(await page.content())
            
            self.id += 1
            self.limit -= 1
            
            if (self.limit == 0):
                return
            
            anchors = await page.querySelectorAll('a')
            newLinks: list[str] = []
            
            for anchor in anchors:
                newLink: str = await page.evaluate('(element) => element.href', anchor)
                newLinks.append(newLink)
                            
            for newLink in newLinks:
                newUrlParse = urlparse(newLink)
                newParsedLink = newUrlParse.scheme + "://" + newUrlParse.netloc + newUrlParse.path
                if newParsedLink in self.visited:
                    continue
                await self.crawl(page, newParsedLink)
                if (self.limit == 0):
                    return
        except:
            print("Error has occurred!")
            self.limit = 0
            
    async def extractText(self, html: str):
        bs4 = BeautifulSoup(html, 'html.parser')
        text = bs4.find_all(text=True)
        output = ''
        for t in text:
            if (t.parent.name not in self.blacklist):
                content = str('{}'.format(t))
                output += ' '.join(content.split()) + ' '
        try:
            file = open('pages/' + str(self.id) + '.txt', 'w')
            file.write(output)
            file.close()
        except:
            print('cannot open file ' + str(self.id) + '.txt')
                                                      

    async def startCrawling(self):
        browser = await pt.launch()
        page = await browser.newPage()
        await self.crawl(page, self.startUrl)
    
    
crawler = Crawler(Url, 90)
asyncio.get_event_loop().run_until_complete(crawler.startCrawling())