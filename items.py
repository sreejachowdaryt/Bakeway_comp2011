from app import db
from app.models import Product

# Add sample products
cakes = [
    {
        "name": "Carrot Orange Cake",
        "description": "The cake is made of zest of orange and lime that makes the cake even more delicious.",
        "price": 5.0,
        "category": "Cake",
        "image": "images/carrot-orange-cake.jpg",
        "stock": 10 
    },
    {
        "name": "Chocolate Fudge Cake",
        "description": "Rich chocolate fudge cake made with the finest cocoa and topped with ganache.",
        "price": 6.5,
        "category": "Cake",
        "image": "images/chocolate.jpg",
        "stock": 10 
    },
    {
        "name": "Lemon Drizzle Cake",
        "description": "A zesty and moist lemon cake topped with a tangy lemon glaze.",
        "price": 6.5,
        "category": "Cake",
        "image": "images/lemon-rizzle.jpg",
        "stock": 10 
    },
    {
        "name": "Red Velvet Cake",
        "description": "A classic red velvet cake with layers of cream cheese frosting.",
        "price": 7.0,
        "category": "Cake",
        "image": "images/red-velvet.jpg",
        "stock": 10 
    },
    {
        "name": "Victoria Sponge Cake",
        "description": "A light sponge cake filled with strawberry jam and whipped cream.",
        "price": 5.5,
        "category": "Cake",
        "image": "images/victoria-sponge.jpg",
        "stock": 10 
    },
    {
        "name": "Plum Picnic Cake",
        "description": "We used beautiful plums, but this recipe is great for all kinds of fruit, and takes no time to put together.",
        "price": 4,
        "category": "Cake",
        "image": "images/plum-picnic-cake.jpg",
        "stock": 10 
    },
    {
        "name": "Strawberry White Chocolate Almond Cake",
        "description": "Deleciously prepared with rich and fresh strawberries and white chocolate almomd.",
        "price": 7.5,
        "category": "Cake",
        "image": "images/Strawberry.jpg",
        "stock": 10 
    },
    {
        "name": "Coffee Cake",
        "description": "Made out of freshly grounded coffee beans and touch of vanilla esscense perfect tea-time treat for coffee lovers.",
        "price": 5.5,
        "category": "Cake",
        "image": "images/coffee-cake.jpg",
        "stock": 10 
    },
    {
        "name": "Banana Walnut Loaf Cake",
        "description": "Combination of ripped bananas and walnuts.",
        "price": 5.5,
        "category": "Cake",
        "image": "images/banana-walnut.jpg",
        "stock": 10 
    }
]

cookies = [
    {
        "name": "Chocolate Chip Cookies",
        "description": " Classic crunchy chocolate chip cookie.",
        "price": 2.5,
        "category": "Cookie",
        "image": "images/chocochip.jpg",
        "stock": 10 
    },
    {
        "name": "Oatmeal Raisin Cookies",
        "description": " Healthy cookies made out of oatmeal and rainisns.",
        "price": 3,
        "category": "Cookie",
        "image": "images/oatmeal.jpg",
        "stock": 10 
    },
    {
        "name": "Shortbread Cookies",
        "description": "Shortbread cookies have a very high ratio of butter or shortening to flour, hence the name.These classic cookies originated in Scotland.",
        "price": 3.3,
        "category": "Cookie",
        "image": "images/shortbread.jpg",
        "stock": 10 
    },
    {
        "name": "Whoopie Pies ",
        "description": "These sandwich-style cookies are made with two soft, pillowy cookies and a marshmallow filling.",
        "price": 3.5,
        "category": "Cookie",
        "image": "images/Whoopie-pie.jpg",
        "stock": 10 
    },
    {
        "name": "Butter Cookies",
        "description": "Made with a smoothy blend of butter and sugar giving a soft texture.",
        "price": 2.7,
        "category": "Cookie",
        "image": "images/butter.jpg",
        "stock": 10 
    },
    {
        "name": "Snowball Cookies",
        "description": "They're balls of buttery shortbread filled with pecans and rolled with powdered sugar.",
        "price": 3,
        "category": "Cookie",
        "image": "images/snowball.jpg",
        "stock": 10 
    },
    {
        "name": "Macaroons",
        "description": "A macaroon is coconut based with dense and lumpy texture. These cookies can be flavored with fruit or dipped in chocolate or simply enjoyed plain.",
        "price": 3.5,
        "category": "Cookie",
        "image": "images/Macaroons.jpg",
        "stock": 10 
    },
    {
        "name": "Fortune Cookies",
        "description": "A crisp and sugary cookie wafer made from flour, sugar, vanilla, and sesame seed oil.",
        "price": 2,
        "category": "Cookie",
        "image": "images/Fortune.jpg",
        "stock": 10 
    },
    {
        "name": "Gingerbread Cookies ",
        "description": "Made with a slight touch of ginger and can be enjoyed with hot chocolate during a cold weather.",
        "price": 3.7,
        "category": "Cookie",
        "image": "images/Gingerbread.jpg",
        "stock": 10 
    }
]

chocolates = [
    {
        "name": "Dark Chocolate Truffles",
        "description": " Made with a filling of rich dark chocolate - Box of 10 truffles",
        "price": 5.5,
        "category": "Chocolate",
        "image": "images/dark-chocolate.jpg",
        "stock": 10 
    },
    {
        "name": "Milk Chocolate Box",
        "description": "Box of milk chocolate truffles",
        "price": 5,
        "category": "Chocolate",
        "image": "images/Milk-chocolate.jpg",
        "stock": 10 
    },
    {
        "name": "Strawberry Chocolate",
        "description": "Strawberreys coated with a thick layer of white chocolate - Box of 10",
        "price": 5,
        "category": "Chocolate",
        "image": "images/Strawberry-chocolate.jpg",
        "stock": 10 
    },
    {
        "name": "Salted Caramel Chocolate",
        "description": " Mix of milk chocolate a caramel",
        "price": 2.7,
        "category": "Chocolate",
        "image": "images/salted-caramel.jpg",
        "stock": 10 
    },
    {
        "name": "Chocolate Orange Truffles",
        "description": "Box of 10 all time favorite orange chocolate truffles",
        "price": 6,
        "category": "Chocolate",
        "image": "images/orange-chocolate.jpg",
        "stock": 10 
    },
    {
        "name": "Assorted Chocolate Box",
        "description": "Box of 10 various flavoured chocolates",
        "price": 6,
        "category": "Chocolate",
        "image": "images/assorted-chocolate.jpg",
        "stock": 10 
    }
]

indian_desserts = [
    {
        "name": "Gulab Jamun",
        "description": "Donuts dunked in rose sugar water making is meltingly soft.",
        "price": 4,
        "category": "Dessert",
        "image": "images/Gulab-Jamun.jpg",
        "stock": 10 
    },
    {
        "name": "Rasmalai",
        "description": "Traditional rasmalai made with chenna or paneer soaked in sugar(cottage cheese), milk and spices like saffron and cardamom.",
        "price": 3,
        "category": "Dessert",
        "image": "images/Rasmalai.jpg",
        "stock": 10 
    },
    {
        "name": "Jalebi",
        "description": "Jalebi as the equivalent to American funnel cakes: fried, crispy and sugar-coated, goes best with rabdi.",
        "price": 3.3,
        "category": "Dessert",
        "image": "images/Jalebi.jpg",
        "stock": 10 
    },
    {
        "name": "Rabdi",
        "description": "Condnesed milk along with sugar, cardamom powder and saffrom.",
        "price": 3.3,
        "category": "Dessert",
        "image": "images/Rabdi.jpg",
        "stock": 10 
    },
    {
        "name": "Kalakand",
        "description": "Sweet chesse fudge similar to an italian chesscak. Flavoured with cardamom and saffron and topped with few assorted nuts.",
        "price": 3.3,
        "category": "Dessert",
        "image": "images/Kalakand.jpg",
        "stock": 10 
    },
    {
        "name": "Malpua",
        "description": "Fried pancakes dunked in sugary, sweet syrup.",
        "price": 3.3,
        "category": "Dessert",
        "image": "images/Malpua.jpg",
        "stock": 10 
    },
    {
        "name": "Mysore Pak",
        "description": "Made of generous amounts of ghee, sugar, gram flour and cardamom to enhance the taste.",
        "price": 3.3,
        "category": "Dessert",
        "image": "images/Mysore-pak.jpg",
        "stock": 10 
    },
    {
        "name": "Kaju Katli",
        "description": "Barfi made with thickening milk and sugar topped with dry fruits and mild spices.",
        "price": 3.3,
        "category": "Dessert",
        "image": "images/kaju-barfi.jpg",
        "stock": 10 
    },
    {
        "name": "Besan Laddoo",
        "description": " Besan laddoo is golden colour from roasting ghee (clarified butter) and besan (chickpea flour) over heat.",
        "price": 3.3,
        "category": "Dessert",
        "image": "images/beasan-laddoo.jpg",
        "stock": 10 
    }
]

products = cakes + cookies + chocolates + indian_desserts

#clear existing products
Product.query.delete()

# Then, update this section to handle the stock value
for product_data in products:
    # Clean and standardize data
    name = product_data["name"].strip()
    category = product_data["category"].strip()
    stock = product_data.get("stock", 0)

    # Check for existing product
    existing_product = Product.query.filter_by(name=name, category=category).first()
    
    if existing_product:
        # Update existing product
        existing_product.description = product_data["description"]
        existing_product.price = product_data["price"]
        existing_product.image = product_data["image"]
        existing_product.stock = stock  # Update stock
    else:
        # Add new product
        new_product = Product(
            name=name,
            description=product_data["description"],
            price=product_data["price"],
            category=category,
            image=product_data["image"],
            stock=stock  # Set initial stock
        )
        db.session.add(new_product)

    # Commit the transaction with error handling
try:
    db.session.commit()
    print("Products added/updated successfully!")
except Exception as e:
    db.session.rollback()
    print(f"Error: {e}")
