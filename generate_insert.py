# for populating tables. gets a snapshot of the most recent 1000 auctions and all referenced players/profiles

import requests
import time

api_key = '51a8d118-dcbc-4145-93d1-00d20febfd59'

def getFromAPI(url):
    response = requests.get(url)
    if response.status_code == 429:
        print("API rate limit exceeded, sleeping for 5 minutes")
        print(response.json())
        time.sleep(300)
        return getFromAPI(url)
    if response.status_code != 200:
        return None
    response_data = response.json()
    return response_data


# this is definitely not good code but i couldn't get sqlalchemy working
# i'll try doing it with ORM stuff this summer maybe
def formatInsert(table, data):
    if table == 'Player':
        column_names = ['uuid', 'username']
        values = [
            f"UUID_TO_BIN('{data['player']['uuid']}')",
            f"'{data['player']['displayname']}'"
        ]
    elif table == 'Profile':
        column_names = ['profile_id', 'player_id', 'join_date']
        join_timestamp = data[1]['profile']['members'][data[0]]['profile']['first_join']
        join_date = time.strftime('%Y-%m-%d', time.localtime(join_timestamp/1000))
        values = [
            f"UUID_TO_BIN('{data[1]['profile']['profile_id'].replace('-','')}')",
            f"UUID_TO_BIN('{data[0]}')",
            f"'{join_date}'"
        ]
    elif table == 'Auction':
        column_names = ['auction_id', 'player_id', 'profile_id', 'item_name', 'category', 'rarity', 'start_bid', 'start_time', 'end_time']
        values = [
            f"UUID_TO_BIN('{data['uuid']}')",
            f"UUID_TO_BIN('{data['auctioneer']}')",
            f"UUID_TO_BIN('{data['profile_id']}')",
            f"'{data['item_name'].replace("'", "''")}'",
            f"'{data['category']}'",
            f"'{data['tier']}'",
            f"{data['bin']}",
            f"{data['starting_bid']}",
            f"{data['start']}",
            f"{data['end']}"
        ]
    elif table == 'Bid':
        column_names = ['auction_id', 'player_id', 'profile_id', 'amount', 'time']
        values = [
            f"UUID_TO_BIN('{data['auction_id']}')",
            f"UUID_TO_BIN('{data['bidder']}')",
            f"UUID_TO_BIN('{data['profile_id']}')",
            f"{data['amount']}",
            f"{data['timestamp']}"
        ]
    else:
        return None
    sql_values = f'({','.join(values)})'

    return sql_values


def generateInserts():
    auctions = getFromAPI('https://api.hypixel.net/v2/skyblock/auctions')
    if auctions is None:
         return

    column_names = {
        'Player': ['uuid', 'username'],
        'Profile': ['profile_id', 'player_id', 'join_date'],
        'Auction': ['auction_id', 'player_id', 'profile_id', 'item_name', 'category', 'rarity', 'bin', 'start_bid',
                    'start_time', 'end_time'],
        'Bid': ['auction_id', 'player_id', 'profile_id', 'amount', 'time']
    }

    player_contents = ''
    profile_contents = ''
    auction_contents = ''
    bid_contents = ''

    player_set = set()
    profile_set = set()
    sep = '\t'
    for auc in auctions['auctions']:
        if auc['auctioneer'] not in player_set:
            print('count:', len(player_set))
            player_set.add(auc['auctioneer'])
            player_data = getFromAPI(f"https://api.hypixel.net/v2/player?key={api_key}&uuid={auc['auctioneer']}")
            player_contents += sep + formatInsert('Player', player_data)
            if (auc['auctioneer'], auc['profile_id']) not in profile_set:
                profile_set.add((auc['auctioneer'], auc['profile_id']))
                profile_data = getFromAPI(f"https://api.hypixel.net/v2/skyblock/profile?key={api_key}&profile={auc['profile_id']}")
                profile_contents += sep + formatInsert('Profile', (auc['auctioneer'], profile_data))
        auction_contents += sep + formatInsert('Auction', auc)
        for bid in auc['bids']:
            if bid['bidder'] not in player_set:
                print('count:', len(player_set))
                player_set.add(bid['bidder'])
                player_data = getFromAPI(f"https://api.hypixel.net/v2/player?key={api_key}&uuid={bid['bidder']}")
                player_contents += sep + formatInsert('Player', player_data)
                if (bid['bidder'], bid['profile_id']) not in profile_set:
                    profile_set.add((bid['bidder'], bid['profile_id']))
                    profile_data = getFromAPI(f"https://api.hypixel.net/v2/skyblock/profile?key={api_key}&profile={bid['profile_id']}")
                    profile_contents += sep + formatInsert('Profile', (bid['bidder'], profile_data))
            bid_contents += sep + formatInsert('Bid', bid)
        sep = ',\n\t'
    with open('./sql/insert.sql', 'w') as f:
        f.write(f'INSERT INTO Player ({','.join(column_names['Player'])})\nVALUES\n')
        f.write(player_contents)
        f.write(f';\nINSERT INTO Profile ({','.join(column_names['Profile'])})\nVALUES\n')
        f.write(profile_contents)
        f.write(f';\nINSERT INTO Auction ({','.join(column_names['Auction'])})\nVALUES\n')
        f.write(auction_contents)
        f.write(f';\nINSERT INTO Bid ({','.join(column_names["Bid"])})\nVALUES\n')
        f.write(bid_contents)
        f.write(f';')

#eb9866bc3879413a85139bfbc3809a46
#print(getFromAPI('https://api.hypixel.net/v2/skyblock/profiles?key=a031c41c-966c-4f61-9822-352c98f8b9d0&uuid=eb9866bc3879413a85139bfbc3809a46')['profiles'][0]['profile_id'])
#print(getFromAPI(f'https://api.hypixel.net/v2/skyblock/profile?key={api_key}&profile=75a1e1dfa228487a9cb94a088a72298f')['profile']['members']['eb9866bc3879413a85139bfbc3809a46']['profile']['first_join'])

# generateInserts()