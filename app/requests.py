import urllib.request,json
# base_url = None
def get_quotes():
    get_quotes_url = 'http://quotes.stormconsultancy.co.uk/random.json'
    with urllib.request.urlopen(get_quotes_url) as url:
        quotes = url.read()
        get_quotes_response = json.loads(quotes)
    return get_quotes_response