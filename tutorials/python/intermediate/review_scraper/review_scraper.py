from requests_html import HTMLSession
import json

sess = HTMLSession()

def get_reviews(url):    
    reviews_list = {"reviews":[], 'url':url}
    res = sess.get(url)
    html = res.html
    reviews = html.find('.product_reviews', first=True).find('[class="review_section"]')
    for review in reviews:
        try:
            review_body = review.find('.blurb_expanded', first=True).text
        except AttributeError:
            review_body = review.find('.review_body', first=True).text
        reviews_list['reviews'].append({
              'author': review.find('.name', first=True).text
            , 'review': review_body
            , 'date': review.find('.date', first=True).text
            , 'score': int(review.find('.review_grade', first=True).text)
            })
    next_page = html.find('.flipper.next', first=True)
    if next_page:
        try:
            next_page_url = next_page.absolute_links.pop() 
            reviews_list['reviews'].extend(get_reviews(next_page_url)['reviews'])
        except KeyError:
            pass
    return reviews_list

url = 'https://www.metacritic.com/tv/obi-wan-kenobi/season-1/user-reviews'
with open('reviews.json', 'w') as f:
    json.dump(get_reviews(url), f)