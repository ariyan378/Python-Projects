from datetime import datetime

from collections import defaultdict

class Product:
    
    def __init__(self, name , category,price):
        
        self.name = name 
        self.category = category
        self.price = price
    
    def __str__(self):
        return f' {self.name} | Category : {self.category} | Price : {self.price}'

class Sale:
    
    def __init__(self , sale_id , product ,quantity , date_str):
        
     self.sale_id = sale_id
     self.product=product
     self.quantity = quantity
     
     self.date = datetime.strptime(date_str ,"%d-%m-%Y" )
     
    def get_revenue(self):
        
        return self.quantity*self.product.price
    
    def __str__(self):
        return ( f'Sale {self.sale_id} -> {self.product}'
                 f" x{self.quantity} Units"
                 f' = {self.get_revenue} TK'
                 f" On {self.date.strftime('%B %d %Y')}"
                )
    
