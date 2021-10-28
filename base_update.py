from bs4 import BeautifulSoup
import requests
import json
import datetime

# TODO add card functions here to there are built directly into the core.json information from the get-go
# if there is no function publically stated ... 'no function published to date'

dicts = []
just_ids = []

for cardID in range(1,1000):
    
    url = 'https://parallel.life/cards/' + str(cardID) + '/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    if len(soup.select('h3')) > 0:
        
        name = soup.select('title')
        h3s = soup.select('h3')
        
        for i, pp in enumerate(soup.select('p')):
            if "Edition of" in pp.text:
                supply_p = pp.text
                break
            
        part1 = soup.select('img')[1]['src'].split('card-art/')[1].split('_')[0].lower()
        if part1 in ['universal', 'kathari', 'marcolian', 'earthen', 'augencore', 'shroud']:
            parallel_name = part1
        else:
            parallel_name = 'none'

            
        d = {'name': name[0].text.lower().replace('parallel masterpiece // alpha // ','').strip(),
            'parallel': parallel_name,
            'description': h3s[1].text,
            'rarity': supply_p.split(' // ')[0].strip(),
            'supply': int(supply_p.split('// Edition of ')[1].strip()),
            'parallel_id': str(cardID),
            'parallel_img': soup.select('img')[1]['src']
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

        if '[PL]' in d['name']:
            d['perfect_loop'] = 1
        else: 
            d['perfect_loop'] = 1

        night_substring_list = ['Night', 'night', 'Ngt']
        if any(map(d['parallel_img'].__contains__, night_substring_list)):
            d['night'] = 1
        else: 
            d['night'] = 0
        
        day_substring_list = ['Day', 'day']
        if any(map(d['parallel_img'].__contains__, day_substring_list)):
            d['day'] = 1
        else:
            d['day'] = 0

        dicts.append(d)
        just_ids.append(d['opensea_id'])


with open('core.json', 'w') as fout:
    json.dump(dicts, fout)


with open('os_ids.json', 'w') as fout:
    json.dump(just_ids, fout)
    
    
# Open a file with access mode 'a'
file_object = open('commit_logs.txt', 'a')
# Append 'hello' at the end of file
file_object.write(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + " | " + str(len(dicts)) + " cards \n")
# Close the file
file_object.close()


