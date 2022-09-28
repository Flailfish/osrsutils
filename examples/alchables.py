from osrsutils.osrsitems import search_item_data, get_current_price
import time

nature_rune = 561
nature_rune_price = get_current_price(nature_rune)

print('Nature rune price: ' + str(nature_rune_price))
results = []
#find every battlestaff that has an high alch profit/loss of no less than -10
for item in search_item_data(name='battlestaff'):
    time.sleep(0.5) #unfortunately we have to have a delay as to not spam the api
    difference = (item['highalch'] - nature_rune_price) - get_current_price(item['id'])
    if(difference >= -10):
        results.append((item['name'], difference))

print(*results,sep='\n')





