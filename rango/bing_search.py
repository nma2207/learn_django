import requests

BING_API_KEY = 'ec5465582f0a4d9e9c21d16717234341'

def run_query(search_term):
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
    #search_term = "Python"

    headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
    params = {'q': search_term, "textDecorations": True, "textFormat": "HTML"}
    results = []

    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_result = response.json()
        for v in search_result['webPages']['value']:
            results.append({
                'title': v['name'],
                'link': v['url'],
                'summary': v['snippet']
            })
    except:
        print("Bing research api error")
    return results