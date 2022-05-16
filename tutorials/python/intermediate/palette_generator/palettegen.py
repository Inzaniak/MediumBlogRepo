import requests_html
import colorgram
import os
from math import sqrt

API_KEY = 'INSERT_YOUR_API_KEY'
URL = 'https://pixabay.com/api/?key={key}&q={q}'
QUERY = 'sea'

colors = open(R'.\data\colors.txt','r',encoding='utf-8').read().split('\n')
colors = [c.split('\t') for c in colors]
colors = [[c[0],tuple(int(c[1][1:][i:i+2], 16) for i in (0, 2 ,4))] for c in colors]

def get_color(clr):
    """Get the closest color from the list of colors

    Args:
        clr (list): The rgb values of the color

    Returns:
        str: The name of the color
    """
    best = ['ND',1000]
    for c in colors:
        clr_el = sqrt( (c[1][0] - clr[0])**2 + (c[1][1] - clr[1])**2 + (c[1][2] - clr[2])**2 )
        if clr_el < best[1]:
            best[0] = c[0]
            best[1] = clr_el
    return best

# Download
rows = []
ses = requests_html.HTMLSession()
res = ses.get(URL.format(key=API_KEY,q=QUERY))
for num,r in enumerate(res.json()['hits']):
    print(r['webformatURL'])
    img = ses.get(r['webformatURL']).content
    open(f'data/img/{num}.jpg', 'wb').write(img)

# Extract
for img in os.listdir('data/img'):
    print(img)
    palette = colorgram.extract(f'data/img/{img}', 5)
    row = open('html/template/palette.html','r',encoding='utf-8').read()
    try:
        rows.append(row.format(
              color1=f"rgb({palette[0].rgb.r},{palette[0].rgb.g},{palette[0].rgb.b})"
            , color2=f"rgb({palette[1].rgb.r},{palette[1].rgb.g},{palette[1].rgb.b})"
            , color3=f"rgb({palette[2].rgb.r},{palette[2].rgb.g},{palette[2].rgb.b})"
            , color4=f"rgb({palette[3].rgb.r},{palette[3].rgb.g},{palette[3].rgb.b})"
            , color5=f"rgb({palette[4].rgb.r},{palette[4].rgb.g},{palette[4].rgb.b})"
            , colorname1=get_color([palette[0].rgb.r, palette[0].rgb.g, palette[0].rgb.b])[0]
            , colorname2=get_color([palette[1].rgb.r, palette[1].rgb.g, palette[1].rgb.b])[0]
            , colorname3=get_color([palette[2].rgb.r, palette[2].rgb.g, palette[2].rgb.b])[0]
            , colorname4=get_color([palette[3].rgb.r, palette[3].rgb.g, palette[3].rgb.b])[0]
            , colorname5=get_color([palette[4].rgb.r, palette[4].rgb.g, palette[4].rgb.b])[0])
        )

    except Exception as e:
        print('Not Enough Colors!')

# Write the results
open(f'html/{QUERY}.html', 'w', encoding='utf-8').write(
    open('html/template/rows_page.html', 'r', encoding='utf-8').read().replace('|rows|', '\n'.join(rows))
)
