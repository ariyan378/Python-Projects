from datetime import datetime
from collections import defaultdict

class Product:
    def __init__(self, name, category, price):
        self.name = name
        self.category = category
        self.price = price

    def __str__(self):
        return f'{self.name} | Category: {self.category} | Price: {self.price}'


class Sale:
    def __init__(self, sale_id, product, quantity, date_str):
        self.sale_id = sale_id
        self.product = product
        self.quantity = quantity
        self.date = datetime.strptime(date_str, "%Y-%m-%d")

    def get_revenue(self):
        return self.quantity * self.product.price

    def __str__(self):
        return (f'Sale {self.sale_id} -> {self.product}'
                f" x{self.quantity} Units"
                f' = {self.get_revenue()} TK'          
                f" On {self.date.strftime('%B %d %Y')}")


class Sales_analytics:                                 
    def __init__(self, lists_of_sale):
        self.sales = lists_of_sale

    def total_revenue(self):
        total = 0
        for i in self.sales:
            total += i.get_revenue()                   
        return total

    def revenue_by_category(self):
        category_totals = defaultdict(float)
        for sale in self.sales:
            category = sale.product.category
            category_totals[category] += sale.get_revenue()  
        return dict(sorted(category_totals.items(), key=lambda x: x[1], reverse=True))

    def top_product(self, how_many=3):
        product_totals = defaultdict(float)
        for sale in self.sales:
            product_totals[sale.product.name] += sale.get_revenue()  
        ranked = sorted(product_totals.items(), key=lambda x: x[1], reverse=True)  
        return ranked[:how_many]
    
    def lowest_product(self , how_many=3):
        
        products = defaultdict(float)
        for sale in self.sales:
            products[sale.product.name]+= sale.get_revenue()
        
        rankeds = sorted(products.items() , key=lambda x: x[1])
        
        return rankeds[:how_many]    

    def monthly_trend(self):
        monthly = defaultdict(float)
        for sale in self.sales:
            month_key = sale.date.strftime("%Y-%m")     
            monthly[month_key] += sale.get_revenue()  
        return dict(sorted(monthly.items()))

    def average_order_value(self):
        if len(self.sales) == 0:
            return 0
        return self.total_revenue() / len(self.sales)

    def print_report(self):
        print()
        print("=" * 52)
        print("        📊 SALES ANALYTICS SUMMARY REPORT")
        print("=" * 52)
        print(f"\n  Total Transactions : {len(self.sales)}")
        print(f"  Total Revenue      : ${self.total_revenue():,.2f}")
        print(f"  Avg Sale Value     : ${self.average_order_value():,.2f}")

        print("\n  📦 Revenue by Category:")
        for category, revenue in self.revenue_by_category().items():
            print(f'   -> {category} : {revenue:,.2f}')

        print("  🏆 TOP 3 Best-Selling Products:")
        for rank, (product_name, revenue) in enumerate(self.top_product(), start=1): 
            print(f'   {rank}. {product_name:<20} ${revenue:,.2f}')
            
        print( " Lowest Selling Among them : Top 3 ")
        
        for rankeds ,(product_name , revenue) in enumerate(self.lowest_product(),start= 1):
            print(f'{rankeds} . {product_name} -> {revenue:,.2f}Tk')    

        print("\n" + "=" * 25)
        
        
if __name__ == "__main__":


    laptop      = Product("Laptop",       "Electronics", 1200)
    chair       = Product("Desk Chair",   "Furniture",    350)
    python_book = Product("Python Book",  "Education",     45)
    headphones  = Product("Headphones",   "Electronics",  199)
    desk        = Product("Standing Desk","Furniture",    600)

    print("\n  ✅ Products Created:")
    print(" ", laptop)
    print(" ", chair)
    print(" ", python_book)

    all_sales = [
        Sale(1,  laptop,      3,  "2024-01-15"),
        Sale(2,  chair,       5,  "2024-01-20"),
        Sale(3,  python_book, 10, "2024-02-05"),
        Sale(4,  headphones,  7,  "2024-02-18"),
        Sale(5,  laptop,      2,  "2024-03-10"),
        Sale(6,  desk,        4,  "2024-03-22"),
        Sale(7,  python_book, 15, "2024-04-01"),
        Sale(8,  chair,       3,  "2024-04-14"),
        Sale(9,  headphones,  6,  "2024-05-09"),
        Sale(10, laptop,      1,  "2024-05-30"),
    ]

    print("\n  ✅ Sample Sales:")
    for sale in all_sales[:3]:   
        print(" ", sale)

    analytics = Sales_analytics(all_sales)
    analytics.print_report()


    print("\n  🔍 Quick Checks:")
    print(f"     Laptop price      : ${laptop.price}")
    print(f"     Sale #1 revenue   : ${all_sales[0].get_revenue()}")
    print(f"     Total revenue     : ${analytics.total_revenue():,.2f}")        