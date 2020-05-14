import aiohttp
import asyncio
import json
from lxml import etree
import tornado.escape
import tornado.ioloop
import tornado.locks
import tornado.web
import os.path
import uuid
import github_trending

from tornado.options import define, options, parse_command_line


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class GetTrendingHandler(tornado.web.RequestHandler):

    async def get(self):
        result = await github_trending.get_trending()
        self.finish(result)


def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/get-trending", GetTrendingHandler),
        ])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()



if __name__=='__main__':
    main()
