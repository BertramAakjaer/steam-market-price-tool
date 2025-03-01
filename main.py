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
        print(f"{item.name}\t\t{item.price_in_use:.2f} € ({(item.price_in_use + KEY_PRICE):.2f} € with keys)")
        
    print("\n")

def reload_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    header = text2art("Steam Market Tool")
    print(header)
    
def current_amount_prices(steam_items):
    print("\n")
    
    print("Current prices for bought items:")
    
    price_total = 0
    
    for item in steam_items:
        if item.count_for_price != 0:
            print(f"{item.name}({item.count_for_price})    \t {(item.price_in_use + KEY_PRICE) * item.count_for_price:.2f} € \t ({(item.price_in_use + KEY_PRICE):.2f} € each)")
            price_total += (item.price_in_use + KEY_PRICE) * item.count_for_price
    print(f"Total: {price_total:.2f} €")
        
    print("\n")
    

def set_prices_individually(steam_items):
        
    for item in steam_items:
        if item.count_for_price != 0:
            current_amount_prices(steam_items)
            break
        
    while True:
        print("\n")
        print("Choose a case to change number:")
        
        print("[0]\tExit")
        
        for i, item in enumerate(steam_items):
            print(f"[{i+1}]\t{item.name}")
        
        print("\n")
        try:
            choice = int(input(f"Choose(1..{len(steam_items)}): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        
        if choice == 0:
            break
        
        if choice < 1 or choice > len(steam_items):
            print("Invalid choice.")
            print("\n")
            continue
        
        item = steam_items[choice - 1]
        
        print("\n")
        print("Starting price for amount session...")
        print("Write a amount of items (e for exit): ")
        print("\n")
        
        while True:
            a = input("Amount: ")
            
            if a == "e":
                break
            
            if not a.isdigit():
                print("Invalid input.")
                continue
            
            a = int(a)
            
            print("\n")
            print(f"{item.name}({a}) \t {a * (item.price_in_use + KEY_PRICE):.2f} € ({(item.price_in_use + KEY_PRICE):.2f} € each)")
            item.count_for_price = a
            print("(e for exit)")
            
            print("\n")
            
        for item in steam_items:
            if item.count_for_price != 0:
                current_amount_prices(steam_items)
                break
            
        print("\n")

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
        
        try:
            choice = int(input("Choose (1..6): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        
        print("\n")
        
        match choice:
            case 1:
                set_prices_individually(steam_items)
                print("\n")
                
            case 2:
                try:
                    budget = int(input("What is your budget(EUR): "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue
                
                print("\n")
                
                for item in steam_items:
                    print(f"{item.name} - You can buy and open {math.floor(budget/(item.price_in_use + KEY_PRICE))}, costing {math.floor((item.price_in_use + KEY_PRICE) * math.floor(budget/(item.price_in_use + KEY_PRICE))):.2f} €")
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