import requests_html
from sanic import Sanic, json
from sanic.response import text


def get_heroes():
    """Returns the list of heroes from the Dota 2 Wiki

    Returns:
        json: A json containing the list of heroes
    """
    # Load the page
    sess = requests_html.HTMLSession()
    url = 'https://dota2.fandom.com/wiki/Heroes'
    res = sess.get(url)
    # Retrieve the table
    table = res.html.find('tbody', first=True)
    table_urls = table.find('a')
    table_urls = [x.absolute_links.pop() for x in table_urls]
    # Clean data from strength, agility, intelligence
    to_clean = ['Strength', 'Agility', 'Intelligence']
    for i in to_clean:
        table_urls = [x for x in table_urls if i not in x]
    # Create the output
    output = {"heroes": []}
    for entry in table_urls:
        output["heroes"].append(
            {
               "name": entry.split('/')[-1]
             , "clean_name": entry.split('/')[-1].replace('_',' ')
             , "url": entry
             }
            )
    return output

def get_hero(hero_name):
    """Returns the hero's information from the Dota 2 Wiki

    Args:
        hero_name (str): The hero's name

    Returns:
        json: A json containing the hero's information
    """
    # Load the page
    sess = requests_html.HTMLSession()
    url = 'https://dota2.fandom.com/wiki/' + hero_name
    res = sess.get(url)
    # Retrieve the table
    table = res.html.find('.infobox', first=True)
    # Populate data variables
    name = table.find('th', first=True).text.split('\n')[0]
    stats = table.find('th', first=True).text.split('\n')[1:]
    img_url = table.find('th', first=True).find('a', first=True).attrs['href']
    sub_table = table.find('table.evenrowsgray', first=True)
    rows = sub_table.find('tr')
    # Create the output
    out_rows = []
    for row in rows:
        if row.find('a', first=True):
            out_rows.append(row.text.split('\n'))   
    # DATA CLEANING
    check_list = ['L0','L1','L25','Level']
    out_rows = [x for x in out_rows if x[0] not in check_list]
    out_rows = [x for x in out_rows if len(x) > 1]
    out_rows = [[y for y in x if y not in ('Link','▶️','')] for x in out_rows]
    hero_out = {
          "name": name
        , "imgUrl": img_url
        , "stats": {"str": stats[0], "agi": stats[1], "int": stats[2]}
        , "health": {"LVL0":out_rows[0][1], "LVL1":out_rows[0][2], "LVL15":out_rows[0][3], "LVL25":out_rows[0][4], "LVL30":out_rows[0][5]}
        , "mana": {"LVL0":out_rows[1][1], "LVL1":out_rows[1][2], "LVL15":out_rows[1][3], "LVL25":out_rows[1][4], "LVL30":out_rows[1][5]}
        , "armor": {"LVL0":out_rows[2][1], "LVL1":out_rows[2][2], "LVL15":out_rows[2][3], "LVL25":out_rows[2][4], "LVL30":out_rows[2][5]}
        , "damageBlock": out_rows[3][1]
        , "magicResistance": out_rows[4][1]
        , "statusResistance": out_rows[5][1]
        , "damage": {"LVL0":out_rows[6][1], "LVL1":out_rows[6][2], "LVL15":out_rows[6][3], "LVL25":out_rows[6][4], "LVL30":out_rows[6][5]}
        , "attackRange": out_rows[7][1]
        , "attackSpeed": out_rows[8][1]
        , "attackAnimation": out_rows[9][1]
        , "projectileSpeed": out_rows[10][1]
        , "movementSpeed": out_rows[11][1]
        , "turnRate": out_rows[12][1]
        , "collisionSize": out_rows[13][1]
        , "visionRange": out_rows[14][2].replace("\xa0•\xa0","-")
        , "legs": out_rows[15][1]
    }
    return hero_out

app = Sanic("WebToAPI")
HOST = "localhost"
PORT = 8000

# Routes
# GET /heroes
@app.route('/heroes')
async def heroes(request):
    return json(get_heroes())

# GET /hero?hero=<hero_name>
@app.get('/hero')
async def hero(request):
    parameters = request.args
    return json(get_hero(parameters['hero'][0]))

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True, auto_reload=True)