import requests_html
from rich import console
import webbrowser

ses = requests_html.HTMLSession()
language = 'en'
console = console.Console()

search_term = console.input("Insert the search term: ")
url = f'https://{language}.wikipedia.org/w/index.php?search={search_term}&fulltext=1&ns0=1'
res = ses.get(url)
results = res.html.find('.mw-search-result')
urls = []
for num,result in enumerate(results):
    title = result.find('.mw-search-result-heading', first=True).text
    summary = result.find('.searchresult', first=True).text
    data = result.find('.mw-search-result-data', first=True).text
    urls.append(result.find('.mw-search-result-heading', first=True).absolute_links.pop())
    console.print(f'[blue]{num}\t{title}\n\t[white]{summary}\n\t[green]{data}\n')
selected_item = int(console.input("Select the number of the article you want to open: "))
webbrowser.open(urls[selected_item])
