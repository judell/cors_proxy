import json, urllib, urlparse, requests, re, traceback, pyramid, pprint, time, os, pickle
from operator import attrgetter
from pyramid.request import Request
from pyramid.request import Response

host = '10.0.0.9'
port = 8000

def cors_helper(request, response=None):
    if response is None:
        response = Response()
    request_headers = request.headers['Access-Control-Request-Headers'].lower()
    request_headers = re.findall('\w(?:[-\w]*\w)', request_headers)
    response_headers = ['access-control-allow-origin']
    for req_acoa_header in request_headers:
        if req_acoa_header not in response_headers:
            response_headers.append(req_acoa_header)
    response_headers = ','.join(response_headers)
    response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '%s' % response_headers
        })
    response.status_int = 204
    print response.headers
    return response

def update(request):
    if  request.method == 'OPTIONS':
        print 'cors preflight'
        return cors_helper(request)
    else:
        qs = urlparse.parse_qs(request.query_string)
        id = qs['id'][0]
        token = qs['token'][0]
        user = qs['user'][0]
        data = request.body
        print id, token, user, data
        headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json;charset=utf-8' }
        r1 = requests.put('https://hypothes.is/api/annotations/' + id, headers=headers, data=data, verify=False)
        print r1.status_code
        print r1.text
        r2 = Response(r1.text)
        r2.headers.update({
            'Access-Control-Allow-Origin': '*'
            })
        return r2

if __name__ == '__main__':

    from wsgiref.simple_server import make_server
    from pyramid.config import Configurator
    from pyramid.response import Response

    config = Configurator()

    config.add_route('update', '/update')
    config.add_view(update, route_name='update')

    app = config.make_wsgi_app()
    server = make_server(host, port, app)
    server.serve_forever()
    

