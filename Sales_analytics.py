from datetime import datetime

from collections import defaultdict

class Product:
    
    def __init__(self, name , category,price):
        
        self.name = name 
        self.category = category
        self.price = price
    
    def __str__(self):
        return f' {self.name} | Category : {self.category} | Price : {self.price}'
    