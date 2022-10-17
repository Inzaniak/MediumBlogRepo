from datetime import datetime
import requests_html
import parsedatetime
sess = requests_html.HTMLSession()

def try_cast(value, cast):
    try:
        return cast(value)
    except ValueError:
        return 0

class Album:
    def __init__(self, in_html):
        self.title = in_html.find('.page_charts_section_charts_item_title', first=True).text
        self.artist = in_html.find('.page_charts_section_charts_item_credited_links_primary', first=True).text
        date_str = in_html.find('.page_charts_section_charts_item_date', first=True).text
        parsed_date, parse_status = parsedatetime.Calendar().parse(date_str)
        self.date = datetime(*parsed_date[:6])
        try:
            self.genres = in_html.find('.page_charts_section_charts_item_genres_primary', first=True).find(".comma_separated")
            self.genres = [x.text for x in self.genres]
        except Exception:
            self.genres = []
        try:
            self.sub_genres = in_html.find('.page_charts_section_charts_item_genres_secondary', first=True).find(".comma_separated")
            self.sub_genres = [x.text for x in self.sub_genres]
        except Exception:
            self.sub_genres = []
        try:
            self.descriptors = in_html.find('.page_charts_section_charts_item_genre_descriptors', first=True).find(".comma_separated")
            self.descriptors = [x.text for x in self.descriptors]
        except Exception:
            self.descriptors = []
        self.average = try_cast(in_html.find('.page_charts_section_charts_item_details_average_num',first=True).text, float)
        self.voters = try_cast(in_html.find('.page_charts_section_charts_item_details_ratings',first=True).find('.full',first=True).text, int)
        self.reviews = try_cast(in_html.find('.page_charts_section_charts_item_details_reviews',first=True).find('.full',first=True).text, int)

    def __str__(self):
        return f'{self.title} by {self.artist} on {self.date} ({self.average} from {self.voters} voters)'

final_els = []
for page in range(1, 10):
    response = sess.get(f'https://rateyourmusic.com/charts/esoteric/album/2022/{page}')
    elements = response.html.find(".page_section_charts_item_wrapper")
    final_els.extend(Album(el) for el in elements)
for el in final_els:
    print(el)

# print top 10 genres
genre_counter = {}
for el in final_els:
    for genre in el.genres:
        if genre in genre_counter:
            genre_counter[genre] += 1
        else:
            genre_counter[genre] = 1
for genre in sorted(genre_counter, key=genre_counter.get, reverse=True)[:10]:
    print(f'{genre}: {genre_counter[genre]}')

# print ambient albums
row_num = 1
for el in final_els:
    if 'ambient' in [x.lower() for x in el.genres]:
        print(f'{row_num}.',el)
        row_num += 1