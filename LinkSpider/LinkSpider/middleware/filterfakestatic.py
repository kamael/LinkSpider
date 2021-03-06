from scrapy.http import Request
from scrapy import log

from LinkSpider.tools.PathSet import PathSet


class FilterFakeStaticMiddleware(object):

    def __init__(self, manager):
        self.manager = manager
        self.pathSet = PathSet()

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler._urlmanager)
        return o

    def process_spider_output(self, response, result, spider):

        def _filter(r):
            if not isinstance(r, Request):
                return True

            url = r.url
            if not self.pathSet.dismatch(url):
                log.msg(format="Filtered pathset repeat %(request)s",
                        level=log.DEBUG, spider=spider, request=r)
                return False
            if not self.manager.addUrl(url):
                log.msg(format="Filtered url repeat %(request)s",
                        level=log.DEBUG, spider=spider, request=r)
                return False

            return True

        return (r for r in result or () if _filter(r))


