class steam_item():
    def __init__(self, name, hash):
        self.name = name
        self.hash = hash

        self.media_price = 0
        self.lowest_price = 0
        
        self.price_in_use = 0
        
        self.__current_price_metric = "median"
        
        self.last_time_search = 0
        
    def setprices(self, media_price, lowest_price):
        self.media_price = float(media_price.replace('€', '').replace(',', '.').replace('-', ''))
        self.lowest_price = float(lowest_price.replace('€', '').replace(',', '.').replace('-', ''))
        
        if self.__current_price_metric == "median":
            self.price_in_use = self.media_price
        else:
            self.price_in_use = self.lowest_price
    
    
    def setPriceFromCache(self, media_price, lowest_price):
        self.media_price = media_price
        self.lowest_price = lowest_price
        
        if self.__current_price_metric == "median":
            self.price_in_use = self.media_price
        else:
            self.price_in_use = self.lowest_price
        
        
    def change_price_metric(self):
        if self.__current_price_metric == "median":
            
            self.__current_price_metric = "lowest"
            self.price_in_use = self.lowest_price
        else:
            
            self.__current_price_metric = "median"
            self.price_in_use = self.media_price
    
    def get_current_price_metric(self):
        return self.__current_price_metric