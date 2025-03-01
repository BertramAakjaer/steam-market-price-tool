import requests, time, random, math, os
from json_parser import get_config
from item_classes import steam_item
from tqdm import tqdm
from art import text2art
import json


KEY_PRICE = 2.35

def populate_price(steam_item):
    appid = "730"
    currency = "3"
        
    url = f"https://steamcommunity.com/market/priceoverview/?appid={appid}&currency={currency}&market_hash_name={steam_item.hash}"
    response = requests.get(url)
    data = response.json()
    
    if data['success']:
        steam_item.setprices(data['median_price'], data['lowest_price'])
    else:
        print(f"Error: {steam_item.name} not found.")
        
    time.sleep(random.randint(2, 3))


def check_price_times(steam_items):
    
    price_cache = {}
    
    # Load price cache from file if it exists
    try:
        with open("price_cache.txt", "r") as f:
            price_cache = json.load(f)
    except FileNotFoundError:
        pass

    with tqdm(steam_items, desc="Loading prices") as pbar:
        for item in pbar:
            if item.hash in price_cache:
                last_time_search, median_price, lowest_price = price_cache[item.hash]
                
                if time.time() - last_time_search > 3600:  # Check if more than an hour old
                    pbar.set_description(f"Loading new price from outdated cache for {item.name}")
                    
                    item.last_time_search = time.time()
                    populate_price(item)
                    
                else:
                    pbar.set_description(f"Loading price from cache for {item.name}")
                                
                    item.setPriceFromCache(median_price, lowest_price)
                    item.last_time_search = last_time_search
                    
            else:
                pbar.set_description(f"Loading new prices for {item.name}")
                
                item.last_time_search = time.time()
                populate_price(item)

    # Save price cache to file
    with open("price_cache.txt", "w") as f:
        json.dump({item.hash: [item.last_time_search, item.media_price, item.lowest_price] for item in steam_items}, f)


def get_prices(steam_items):
    print("\n")
    
    for item in steam_items:
        print(f"{item.name}\t\t{item.price_in_use} € ({(item.price_in_use + KEY_PRICE):.2f} € with keys)")
        
    print("\n")

def reload_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    header = text2art("Steam Market Tool")
    print(header)

def main():
    
    reload_menu()
    
    steam_items = []
    
    conf = get_config()
    
    for name, hash in conf:
        steam_items.append(steam_item(name, hash))
        
    if len(steam_items) == 0:
        print("No items found in config.json.")
        return
        
    check_price_times(steam_items)
        
    print("\n")
    
    while True:
        print("\n")
        print("Choices:")
        print("1. Get price from amount of items")
        print("2. Use budget to show how many items you can buy")
        print("3. Show item prices")
        print("4. Recalculate prices")
        print(f"5. Switch prices (current: {steam_items[0].get_current_price_metric()})")
        print("6. Exit")
        
        print("\n")
        
        choice = int(input("Choose (1..6): "))
        
        print("\n")
        
        match choice:
            case 1:
                print("\n")
            case 2:
                budget = int(input("What is your budget(EUR): "))
                
                print("\n")
                
                for item in steam_items:
                    print(f"{item.name} - You can buy and open {math.floor(budget/(item.price_in_use + KEY_PRICE))}, costing {math.floor((item.price_in_use + KEY_PRICE) * math.floor(budget/(item.price_in_use + KEY_PRICE)))} €")
            case 4:
                with tqdm(steam_items, desc="Recalculating prices") as pbar:
                    for item in pbar:
                        
                        pbar.set_description(f"Recalculating prices for {item.name}")
                        populate_price(item)
                        item.last_time_search = time.time()
                    
                    with open("price_cache.txt", "w") as f:
                        json.dump({item.hash: [item.last_time_search, item.media_price, item.lowest_price] for item in steam_items}, f)
                        
                print("Prices recalculated.")
                print("\n")
                
                reload_menu()
                
            case 3:
                get_prices(steam_items)
                
            case 5:
                for item in steam_items:
                    item.change_price_metric()
                    
                print(f"Prices switched to {steam_items[0].get_current_price_metric()}")
                print("\n")
            
            case 6:
                break
            
            case _:
                print("Invalid choice.")


if __name__ == "__main__":
    main()