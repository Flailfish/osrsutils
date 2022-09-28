"""
Module used to make requests to the oldschool runescape wiki price api

Currently implements the oldschool runescape wiki price api
Information can be found here: https://oldschool.runescape.wiki/w/RuneScape:Real-time_Prices
https://runescape.wiki/w/Application_programming_interface

"""
import requests
from . import fileutils
import inspect

prices_endpoint = 'http://prices.runescape.wiki/api/v1/osrs'
ge_endpoint = 'https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json'
graph_endpoint = 'https://secure.runescape.com/m=itemdb_oldschool/api/graph/'

headers = {
    'User-Agent': 'OSRS item search',
}

item_list = fileutils.get_data_dir() + 'item_data.json'

def _graph_api_request(id):

    """
    Makes a request to the specified route (using the ge endpoint)
    It is not necessary to call this directly, but do it if you wish.
        
        Parameters: 
                    id (int): A integer representing the item id

        Returns: 
                    requests.Response object containing the servers response

    """
    res = requests.get(graph_endpoint + str(id) + '.json', headers=headers)
    res.raise_for_status()
    return res

def _ge_api_request(id):

    """
    Makes a request to the specified route (using the ge endpoint)
    It is not necessary to call this directly, but do it if you wish.
        
        Parameters: 
                    id (int): A integer representing the item id

        Returns: 
                    requests.Response object containing the servers response

    """
    res = requests.get(ge_endpoint, headers=headers, params = {'item':id})
    res.raise_for_status()
    return res

def _prices_api_request(route:str,query_params = None):

    """
    Makes a request to the specified route (using the prices endpoint)
    Not necessary to call
        
        Parameters: 
                    route (str): A string representing the desired route
                    Possible routes: 'latest','5m','1h','timeseries','mapping'

                    query_params: Dict, list or tuple to send as a query string (optional)
                    Default: None


        Returns: 
                    requests.Response object containing the servers response

    """

    res = requests.get('{}/{}'.format(prices_endpoint,route), headers=headers,  params = query_params)
    res.raise_for_status()
    return res

def get_latest_price(id = None):

    """
    Gets the latest high and low G.E price of the item with the specified id.
    If no id is specified, the latest price of every item is returned

        Parameters: 
                    id (int): item id to search (optional)


        Returns: 
                    the servers response (the latest prices) in JSON format

    """

    try:
        result = _prices_api_request('latest',query_params = {'id':id} if id else None)
    except requests.HTTPError:
        return {}
    return result.json()

def get_5m_price(timestamp = None):

    """
    Gets the 5 minute average high and low G.E price for all items
    If no timestamp is specified, the latest price of the last 5 minutes for every item is returned

        Parameters: 
                    timestamp (int): timestamp that is the beginning of the 5 minute period to be averaged

        Returns: 
                    the servers response (5 minute prices) in JSON format

    """

    try:
        result = _prices_api_request('5m',query_params = {'id': id} if timestamp else None)
    except requests.HTTPError:
        return {}
    return result.json()

def get_1h_price(timestamp = None):

     """
     Gets the 1 hour average high and low G.E price for all items
     If no timestamp is specified, the latest average price over the last hour of every item is returned

        Parameters: 
                    timestamp (int): timestamp that is the beginning of the 1 hour period to be averaged

        Returns: 
                    the servers response (1 hour prices) in JSON format

     """

     try:
        result = _prices_api_request('1h',query_params = {'id': id} if timestamp else None)
     except requests.HTTPError:
        return {}
     return result.json()

def get_time_series(id:int,timestep:int):

    """
    Gets the average high and low prices for the item with the specified id, at the interval specified
     
       Parameters: 
                   id (int): item id to search
                   timestep (int): timestamp that is the beginning of the specified period to be averaged
                   valid options are '5m','1h','6h'

       Returns: 
                the servers response in JSON format

    """

    try:
        result = _prices_api_request('timeseries',query_params = {'id':id,'timestep':timestep})
    except requests.HTTPError:
        return {}
    return result.json()

def _get_mapping():

    """

     Gets a mapping of every item in osrs from the wiki api
     mapping is currently an unofficial part of the api - subject to change

        Returns: the servers response in JSON format
                 or an empty collection if some sort of HTTPError occurred

    """

    try:
        result = _prices_api_request('mapping')
    except requests.HTTPError:
        return {}
    return result.json()

def get_item_data():

    """
     Gets a mapping of every item in osrs from the item_data.json file

        Returns: the list as a collection

    """

    return fileutils.read_json(item_list)

def _update_item_data():

    """
    Updates the item_data.json file with the mapping from _get_mapping()
    Used to avoid having to call the api many times
    Technically you can update it as much as you'd like
    but you'll probably get rate-limited if you access the mapping route too much

        Returns: bool (whether list was updated)

    """

    item_mapping = _get_mapping()
    if(item_mapping):
        updated = fileutils.write_to_json(item_list,item_mapping)
    return updated



def ge_lookup(id):

    """
     Looks up an item on the grand exchange
        
        Parameters: id (int): id of item to look up

        Returns: the servers response in JSON format
                 
                 {"icon":"https://secure.runescape.com/m=itemdb_oldschool/1662647178079_obj_sprite.gif?id=4751",
                 "icon_large":"https://secure.runescape.com/m=itemdb_oldschool/1662647178079_obj_big.gif?id=4751",
                 "id":4751,
                 "type":"Default",
                 "typeIcon":"https://www.runescape.com/img/categories/Default",
                 "name":"Torag's platelegs",
                 "description":"Torag the Corrupted's plate leg armour.",
                 "current":{"trend":"neutral","price":"217.1k"},
                 "today":{"trend":"positive","price":"+1,223"},
                 "members":"true",
                 "day30":{"trend":"negative","change":"-5.0%"},
                 "day90":{"trend":"positive","change":"+1.0%"},
                 "day180":{"trend":"negative","change":"-10.0%"}}

    """

    try:
        result = _ge_api_request(id) 
    except requests.HTTPError:
        return {}
    return result.json().get('item')


def get_current_price(id):

    """

    Gets an item's current price from the grand exchange using the osrs graphs
    This is more accurate than getting the price from ge_lookup()
    The price is generally rounded in that case i.e 10.5k instead of 10534

    Parameters:
                id (int): id to search

    Returns: the current price of the item or 0 if the price was unable to be retrieved

    """
    try:
        result = _graph_api_request(id)
    except requests.HTTPError:
        return 0
    return int(next(reversed(result.json().get('daily').values())))



def search_item_data(examine:str = None, id:int = None, members:bool = None,lowalch:int=None,highalch:int=None,
                     limit:int = None, value:int=None,icon:str=None,name:str=None):
    """ 
    Search the mapping data for items matching the query

        Parameters:
        examine (str): Examine text to search for
        id (int): Item id to search for
        members (bool):  Whether to search for member's objects: Omitting this will include both members and non-members objects in the results
        lowalch (int): Low alch price to search for
        highalch (int): High alch price to search for
        limit (int): GE buy limit to search for
        value (int): Item value to search for
        icon (str): Icon file name to search for (This is the file name on the osrs wiki)
        name (str): Item name to search for

        Returns: a list of items matching the search query

    """

    def clean(s):
        if(isinstance(s,str)):
            return s.lower()
        return s

    query = {'examine':examine,'id':id,'members':members,'lowalch':lowalch,'highalch':highalch,
            'limit':limit,'value':value,'icon':icon,'name':name}

    search_query = {k:clean(v) for k, v in query.items() if v is not None}
    results = []

    for item in get_item_data():

        name = search_query.get('name')
        examine = search_query.get('examine')
        icon = search_query.get('icon')
        
        if(name):
            if(name not in str(item.get('name')).lower()):
                continue
   
        if(examine):
            if(examine not in str(item.get('examine')).lower()):
                continue

        if(icon):
            if(icon not in str(item.get('icon')).lower()):
                continue

        if({k:v for k,v in search_query.items() if k not in ('name','examine','icon')}.items() <= {k:v for k,v in item.items()}.items()):
            results.append(item)

    return results


def convert(n:str):

    """

    Converts a number string (like 100k) to a number
        
        Parameters:
                    n (str): String to convert

        Returns: an integer corresponding to the passed string

    """
    n = str(n).replace(',','').lower()
    if('k' in n):
        return int(float(n.replace('k',''))*1000)
    elif('m' in n):
        return int(float(n.replace('m',''))*1000000)
    elif('b' in n):
        return int(float(n.replace('b',''))*1000000000)
    return int(float(n))