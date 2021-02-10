def get_api_key():
    load_dotenv()
    client_ID = os.getenv('CLIENT_ID')
    client_SECRET = os.getenv('CLIENT_SECRET')

    url = 'https://us.battle.net/oauth/token'

	data = {
		'client_id': client_ID,
		'client_secret': client_S,
		'grant_type': 'client_credentials'}

	r = requests.post(url, data)
	key = json.loads(r.text)

	return key

def get_character():
	region = input("Enter your region: ").lower()
	server = input("Enter your server: ").lower()
	server = server.replace(" ", "-").replace("'", "")
	character = input("Enter your character: ").lower()

	return [region, server, character]

def set_guild():
	region = input("Enter your region: ").lower()
	server = input("Enter your server: ").lower()
	server = server.replace(" ", "-").replace("'", "")
	guild = input('Enter your guild name: ').lower()
	guild = guild.replace(" ", "-").replace("'", "")

	return [region, server, guild]

def get_keystone_data(key, profile):
	api_key = key['access_token']
	url = f'https://{profile[0]}.api.blizzard.com/profile/wow/character/{profile[1]}/{profile[2]}/mythic-keystone-profile/season/5?namespace=profile-us&locale=en_US&access_token={api_key}'

	response = requests.get(url)
	data = json.loads(response.text)

	return(data)

def has_ksm(key, profile):
	api_key = key['access_token']
	url = f'https://{profile[0]}.api.blizzard.com/profile/wow/character/{profile[1]}/{profile[2]}/achievements?namespace=profile-us&locale=en_US&access_token={api_key}'

	response = requests.get(url)
	data = json.loads(response.text)

	count = 0
	for i in data["achievements"]:
		count += 1
		if i["id"] > 14533:
			return None
		if 14531 == i["id"]:
			for j in data["achievements"][count:count+1]:
				if 14532 == j["id"]:
					return 'KSM'
			return 'KSC'

def top_two_keys(key, profile):
	api_key = key['access_token']
	url = f'https://{profile[0]}.api.blizzard.com/profile/wow/character/{profile[1]}/{profile[2]}/mythic-keystone-profile/season/5?namespace=profile-us&locale=en_US&access_token={api_key}'

	response = requests.get(url)
	data = json.loads(response.text)

	top_two = {}

	if 'best_runs' in data:
		for i in data['best_runs']:
			level = i["keystone_level"]
			dungeon = i["dungeon"]['name']
			timed = i['is_completed_within_time']

			if dungeon in top_two:
				top_two[dungeon].append((level, timed))
			else:
				top_two[dungeon] = [(level, timed)]
	else:
		dungeons = get_dungeon_list(key)
		for dungeon in dungeons:
			top_two[dungeon] = [(0, False)]

	return top_two

def	top_timed_keys(high_keys):
	timed_keys = {}
	for dungeon in high_keys:
		highest = 0
		for i in high_keys[dungeon]:
			if True in i and i[0] > highest:
				highest = i[0]
		timed_keys[dungeon] = highest

	return timed_keys

def needed_keys(profile, top_timed_keys):
	name = profile[2].title()
	needed = []

	for key in top_timed_keys:
		if top_timed_keys[key] < 15:
			needed.append(key)

	return {name: needed}

def get_player_class(class_id):
	classes = {1:'Warrior', 2:'Paladin', 3:'Hunter', 4:'Rogue', 5:'Priest', 6:'Death Knight', 
				7:'Shaman', 8:'Mage', 9:'Warlock', 10:'Monk', 11:'Druid', 12:'Demon Hunter'}

	return classes[class_id]

def get_dungeon_list(key):
	api_key = key['access_token']
	url = f'https://us.api.blizzard.com/data/wow/mythic-keystone/dungeon/index?namespace=dynamic-us&locale=en_US&access_token={api_key}'

	response = requests.get(url)
	data = json.loads(response.text)

	dungeons = []

	for dungeon in data['dungeons']:
		dungeons.append(dungeon['name'])

	return dungeons

def get_roster(key, guild):
	api_key = key['access_token']
	url = f'https://{guild[0]}.api.blizzard.com/data/wow/guild/{guild[1]}/{guild[2]}/roster?namespace=profile-us&locale=en_US&access_token={api_key}'

	response = requests.get(url)
	data = json.loads(response.text)

	roster = {}

	for i in data['members']:
		name = i['character']['name']
		realm = i['character']['realm']['slug']
		pclass_id =i['character']['playable_class']['id']
		pclass = get_player_class(pclass_id)
		rank = i['rank']

		roster[name] = roster.get(name, {'realm':realm, 'class':pclass, 'rank':rank})
	
	return roster

def prune_roster(roster): # Get only characters of specific ranks
	ranks = []
	rank = True

	while rank:
		print(f'Current ranks are: {ranks}')
		rank = input('Enter rank: (q to quit) ')
		if rank == 'q':
			break
		elif rank in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
			ranks.append(rank)
			continue
		else:
			print('Please enter a valid rank number (1-10)')
			continue

	new_roster = {}
	for i in roster:
		if roster[i]['rank'] in ranks:
			new_roster[i] = new_roster.get(i, roster[i])

	return new_roster

def get_guild_ksm(key, region, roster):
	new_roster = prune_roster(roster)

	keys_needed = {}

	for character in new_roster:
		profile = [region, new_roster[character]['realm'], character.lower()]
		high_keys = top_two_keys(key, profile)
		top_keys = top_timed_keys(high_keys)
		keys = needed_keys(profile, top_keys)

		keys_needed[character] = new_roster[character]
		keys_needed[character]['keys'] = keys[character]

	return keys_needed