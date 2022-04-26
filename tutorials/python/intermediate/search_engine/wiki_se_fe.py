import requests_html
from bottle import Bottle, static_file, request, run, template

ses = requests_html.HTMLSession()

def search(search_term, language = 'en'):
    url = f'https://{language}.wikipedia.org/w/index.php?search={search_term}&fulltext=1&ns0=1'
    res = ses.get(url)
    results = res.html.find('.mw-search-result')
    out_results = []
    for result in results:
        title = result.find('.mw-search-result-heading', first=True).text
        summary = result.find('.searchresult', first=True).text
        data = result.find('.mw-search-result-data', first=True).text
        url = result.find('.mw-search-result-heading', first=True).absolute_links.pop()
        out_results.append({'title': title, 'summary': summary, 'data': data, 'url': url})
    return out_results

app = Bottle()

@app.route('/') # or @route('/login')
def index():
    return open('website/index.html').read()

@app.route('/search')
def index():
    query = request.query['query']
    return template(open('website/search.html').read(), results=search(query))

@app.route('/css/<filename>')
def server_static(filename):
    print('CSS Served')
    return static_file(filename, root='website/css')

@app.route('/js/<filename>')
def server_static(filename):
    print('JS Served')
    return static_file(filename, root='website/js')

@app.route('/images/<filename>')
def server_static(filename):
    print('Image Served')
    return static_file(filename, root='website/images')

print('Serving on http://localhost:8080')
run(app, host='localhost', port=8787, reloader=True)