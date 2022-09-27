"""Module used to make requests to the oldschool runescape hiscores

Currently implements the oldschool runescape 'index_lite' api
Information can be found here: https://runescape.wiki/w/Application_programming_interface#Old_School_Hiscores

Typical usage:

foo = PlayerHiscores(username = 'Foo', account_type = 'UIM')

"""

import requests

class AccountTypeError(Exception):
    """
    An exception raised when an invalid account type is specified
    """
    pass

class HiscoresError(Exception):
    """
    An exception raised when the api fails to return a sufficient response (i.e when it returns status code 400 (user may not exist))
    """
    pass

class PlayerHiscores:

    """
    An object representing a player's hiscore data

    Attributes:
                username (str): A string representing the player's username
                account_type (str): A string representing the player's account type
                ----
                Possible values:
                N: Normal
                IM: Ironman
                UIM: Ultimate ironman
                HCIM: Hardcore ironman
                DMM: Deadman mode
                S: Seasonal - in this case, Leagues
                T: Tournament - probably Deadman tournament
                ----
                skills(dict): A dictionary containing hiscores data for each skill
                Example: {'attack': {'rank':1,'level':99,'xp':200000000},'defence':{'rank':1,'level':99,'xp':200000000}...}
                Every skill is contained in the dictionary.
                Accessing:
                skills['attack']['xp'] would return 200000000
                ----
                bosses(dict): A dictionary containing highscore data for each boss
                Example {'mole':{'rank':100,'kc':1000},'kbd':{'rank':1,'kc':500000}}
                Accessing:
                bosses['kbd']['kc'] would return 500000
                ----
                activities(dict): A dictionary containing highscore data for each activity
                Example: {'leaguepoints':{'rank':34,'value':42},'mediumclues':{'rank':4545,value:'3000'}}
                Accessing:
                activities['mediumclues']['value'] would return 3000
                ----
                A value of -1 for any of the above denotes not ranked


    """

    def __init__(self,username:str,account_type='N'):

        """
        Parameters:
                    username (str): A string representing the player's username
                    account_type (str): A string representing the account type (really is the hiscore table to use)
                    example: IM is ironman hiscores N is normal hiscores

        """

        self.username = username.replace(' ','%20')
        self.account_type = account_type.upper()
        self.skills = {}
        self.activities = {}
        self.bosses = {}
        self._get_player_scores()


    def _get_player_scores(self):

        """
        Searches the hiscores for a player with a username equal to the username attribute
        The exact route (hiscores table ) chosen is determined by the account_type attribute

        Raises:
                AccountTypeError:
                    If an invalid account type is contained in the account_type attribute

                HiscoresError:
                    If the hiscores server responds with a status code other than 200 (HTTP.OK)
                    
        """

        rs = 'http://secure.runescape.com/'

        routes = {
            'N': rs + 'm=hiscore_oldschool/index_lite.ws?player={}'.format(self.username),
            'IM': rs + 'm=hiscore_oldschool_ironman/index_lite.ws?player={}'.format(self.username),
            'UIM': rs + 'm=hiscore_oldschool_ultimate/index_lite.ws?player={}'.format(self.username),
            'HCIM': rs + 'm=hiscore_oldschool_hardcore_ironman/index_lite.ws?player={}'.format(self.username),
            'DMM': rs + 'm=hiscore_oldschool_deadman/index_lite.ws?player={}'.format(self.username),
            'S': rs + 'm=hiscore_oldschool_seasonal/index_lite.ws?player={}'.format(self.username),
            'T': rs + 'm=hiscore_oldschool_tournament/index_lite.ws?player={}'.format(self.username)
            }

        if(self.account_type not in routes.keys()):
            raise AccountTypeError('Invalid account type specified. Valid types: N, IM, UIM, HCIM, DMM')

        response = requests.get(routes[self.account_type])
        if(response.status_code != 200):
            raise HiscoresError("No account with username '{}' found with account type '{}'. Valid types: N, IM, UIM, HCIM, DMM".format(self.username,self.account_type))
        self._parse_hiscores(response.text)

    def _parse_hiscores(self,hiscores):

        """
        Parses the data received from the hiscores api into something the user can actually read

        Sets the skills attribute to a dict with format: {'attack':{'rank':1,'level':99,'xp':200000000}...}
        Sets the bosses attribute to a dict with format: {'kbd':{'rank':1,'kc':344}...}
        Sets the activities attribute to a dict with format: {'mediumclues':{'rank':1,'value':342}...}
                    
        """

        hiscores = hiscores.replace('\n',',').split(',')
        
        self.overall = {'rank':hiscores[0],'level':hiscores[1],'xp':hiscores[2]}

        skills_list = (
                  'attack',
                  'defence',
                  'strength',
                  'hitpoints',
                  'ranged',
                  'prayer',
                  'magic',
                  'cooking',
                  'woodcutting',
                  'fletching',
                  'fishing',
                  'firemaking',
                  'crafting',
                  'smithing',
                  'mining',
                  'herblore',
                  'agility',
                  'thieving',
                  'slayer',
                  'farming',
                  'runecraft',
                  'hunter',
                  'construction'
                  )

        activities_list = (
            'leaguepoints',
            'bhhunter',
            'bhrogue',
            'allclues',
            'beginnerclues',
            'easyclues',
            'mediumclues',
            'hardclues',
            'eliteclues',
            'masterclues',
            'lmsrank',
            'pvprank',
            'swzeal',
            'riftsclosed'
            )

        bosses_list = (
            'sire',
            'hydra',
            'barrows',
            'bryophyta',
            'callisto',
            'cerberus',
            'cox',
            'coxc',
            'chaosele',
            'chaosfanatic',
            'zilyana',
            'corp',
            'crazyarch',
            'prime',
            'rex',
            'supreme',
            'darch',
            'graardor',
            'mole',
            'gg',
            'hespori',
            'kq',
            'kbd',
            'kraken',
            "kree",
            "kril",
            'mimic',
            'nex',
            'nightmare',
            "pnightmare",
            'obor',
            'sarachnis',
            'scorpia',
            'skotizo',
            'tempoross',
            'gauntlet',
            'cgauntlet',
            'tob',
            'tobhard',
            'thermy',
            'toa',
            'toaex',
            'zuk',
            'jad',
            'venenatis',
            "vetion",
            'vorkath',
            'wintertodt',
            'zalcano',
            'zulrah'
            )
        
        for count, skill in enumerate(skills_list):
            self.skills[skill] = {'rank':hiscores[3 + count],'level':hiscores[4 + count],'xp':hiscores[5 + count]}
        

        for count, activity in enumerate(activities_list):
            self.activities[activity] = {'rank':hiscores[3 + len(skills_list)*3 + 2*count],'value':hiscores[4 + len(skills_list)*3 + 2*count]}
        
        
        for count, boss in enumerate(bosses_list):
            self.bosses[boss] = {'rank':hiscores[3 + len(skills_list)*3 + len(activities_list)*2 + 2*count],'kc':hiscores[4 + len(skills_list)*3 + len(activities_list)*2 + 2*count]}