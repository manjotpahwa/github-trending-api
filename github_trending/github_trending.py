import aiohttp
import asyncio
import json
from lxml import etree


BASE_URL = 'https://github.com/'
TRENDING_URL =  'trending?since=today'


class GithubTrending():

    async def get_request(self, session, url: str, headers: dict = None) -> str:
        """
        Async method to get the response.

        Parameters
        ----------
        session: aiohttp.ClientSession
            The session object to use for all the requests.
        url: str
            The URL to fetch the response from.
        headers: dict
            Other options for the request.

        Returns
        -------
        bytes
            The HTTP response for the same.
        """
        async with session.get(url) as resp:
            data = await resp.read()
            return data


    def convertXMLToEtree(self, xml: str) -> dict:
        """
        Convert the XML string object to an Etree element which can easily be
        converted to a JSON dict.

        Parameters
        ----------
        xml: str
            The XML string object or the response from github trending URL.

        Returns
        -------
        lxml.etree object
            The etree.HTML object for the same.
        """
        return etree.HTML(xml)


    async def parse_repo(self, xml: str) -> dict:
        """
        Parse the XML Etree datastructure to a json dict which can be sent.

        Parameters
        ----------
        xml: str
            The etree.HTML object for the response from github trending URL.

        Returns
        -------
        dict
            The response consisting of all the respositories returned and the
            total count.
        """
        repos = []
        articles = xml.xpath('//article')
        for article in articles:
            repo = {'repo': article.xpath('./h1/a/@href')[0][1:]}
            repo['repo_link'] = BASE_URL + repo['repo']
            tmp = article.xpath('./p/text()')
            repo['desc'] = tmp[0].replace('\n', '').strip() if len(tmp) > 0 else ''
            tmp = article.xpath('./div[last()]/span[1]/span[2]/text()')
            repo['lang'] = tmp[0].replace('\n', '').strip() if len(tmp) > 0 else ''
            tmp = article.xpath('./div[last()]/a[1]/text()')
            repo['stars'] = "".join(tmp).replace(' ', '').replace('\n', '')
            tmp = article.xpath('./div[last()]/a[2]/text()')
            repo['forks'] = "".join(tmp).replace(' ', '').replace('\n', '')
            tmp = article.xpath('./div[last()]/span[3]/text()')
            repo['added_stars'] = "".join(tmp).replace('\n', '').strip()
            repo['avatars'] = article.xpath('./div[last()]/span[2]/a/img/@src')
            repos.append(repo)
        return {
            'count': len(repos),
            'repos': repos
        }


    @classmethod
    async def get_trending(cls):
        """
        Get the top most trending repositories from Github for today.

        Returns
        -------
        dict
            The response consisting of all the respositories returned and the
            total count.
        """
        async with aiohttp.ClientSession() as session:
            self = cls()
            resp = await self.get_request(session, BASE_URL + TRENDING_URL)
            resp_etree = self.convertXMLToEtree(resp)
            repos = await self.parse_repo(resp_etree)
        return repos



if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(GithubTrending.get_trending())
#    try:
#        loop.run_forever()
#    finally:
#        loop.run_until_complete(loop.shutdown_asyncgens())
#        loop.close()
