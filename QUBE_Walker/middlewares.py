from scrapy.http import HtmlResponse
import requests                                                              
from requests_ntlm import HttpNtlmAuth

class NTLM_Middleware(object):

    def process_request(self, request, spider):
        url = request.url
        pwd = getattr(spider, 'http_pass', '')
        usr = getattr(spider, 'http_user', '')
        s = requests.session()     
        response = s.get(url, auth=HttpNtlmAuth(usr, pwd))
        return HtmlResponse(url=url, status=response.status_code, headers={}, body=response.content)