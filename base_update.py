from bs4 import BeautifulSoup
import requests
import json
import datetime

dicts = []
just_ids = []

for cardID in range(1,400):
    
    url = 'https://parallel.life/cards/' + str(cardID) + '/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    if len(soup.select('h3')) > 0:
        name = soup.select('title')
        h3s = soup.select('h3')
        supply_p = soup.select('p')[2].text

        h2s = soup.select('h2')        
        
        d = {'name': name[0].text.lower().replace('parallel masterpiece // alpha // ','').strip(),
            'parallel': h3s[0].text,
            'description': h3s[1].text,
            'rarity': supply_p.split(' // ')[0].strip(),
            'supply': int(supply_p.split('// Edition of ')[1].strip()),
            'parallel_id': str(cardID)
            }

        links = soup.select('a')
        for link in links: 
            if 'opensea' in link['href']:
                d['opensea_id'] = link['href'].replace(
                    'https://opensea.io/assets/0x76be3b62873462d2142405439777e971754e8e77/', '')
                
        if len(h3s) > 3:
            d['artist'] = h3s[2].text.split('// @')[1].strip()
        else:
            d['artist'] = ''
        
        if 'Masterpieces' in d['description']:
            d['type'] = 'masterpiece'
        elif 'Card Back' in d['description']:
            d['type'] = 'card back'
        elif 'concept art' in d['name']:
            d['type'] = 'concept art'
        else:
            d['type'] = 'card'

        if '[se]' in d['name']:
            d['standard'] = 'se'
        else:
            d['standard'] = 'standard'

        dicts.append(d)
        just_ids.append(d['opensea_id'])


with open('core.json', 'w') as fout:
    json.dump(dicts, fout)


with open('os_ids.json', 'w') as fout:
    json.dump(just_ids, fout)
    
    
# Open a file with access mode 'a'
file_object = open('commit_logs.txt', 'a')
# Append 'hello' at the end of file
file_object.write(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + " | " + str(len(just_ids)) + " cards \n")
# Close the file
file_object.close()


