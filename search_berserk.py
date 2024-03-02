import requests
from bs4 import BeautifulSoup


class BerserkWeb:
    def __init__(self):
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.3'
        }
        self.url = 'https://readberserk.com/chapter/berserk-chapter-'

    def key_words_search_words(self, user_message):
        # print(user_message)

        # This needs to be changed eventually maybe
        #  it just accounts for "$search "
        usable_message = user_message[8:]
        # print(usable_message)
        if (usable_message.isnumeric()):
            req_chap = int(usable_message)
            if (req_chap > 373 or req_chap < 1):
                print('Searching out of bounds.')
                return "OOB"
            elif (req_chap < 10):
                chap = int(usable_message)
                chap = "00" + str(chap)
                return chap
            elif (req_chap < 100):
                chap = int(usable_message)
                chap = "0" + str(chap)
                return chap
            else:
                chap = int(usable_message)
                chap = str(chap)
                return chap
        else:
            if (len(usable_message) != 2):
                print('Letter chap invalid.')
                return "LCI"
            if (int(usable_message[1]) != 0):
                print('Letter chap invalid.')
                return "LCI"
            else:
                chap = usable_message
                return chap

    def search(self, chap):
        response = requests.get(self.url + chap, headers=self.headers)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        divs = soup.find_all("div", {"class": "img_container mb-2"})
        return divs

    def send_link(self, divs):
        send_link = {}
        # send_link = set()
        i = 0
        for bigDiv in divs:
            children = bigDiv.findChildren("img", recursive=False)
            for child in children:
                # print(child)
                # print(child['src'])
                # send_link.add(str(i) + "|" + child['src'])
                send_link[i] = child['src']
            i = i + 1
        return send_link
