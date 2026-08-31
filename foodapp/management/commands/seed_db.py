import os
import shutil
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.conf import settings
from foodapp.models import Category, FoodItem

class Command(BaseCommand):
    help = 'Seeds the database with 10 categories and ~50 realistic vegetarian food items'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting database seeding...")

        # Create media directories if they don't exist
        media_foods_dir = os.path.join(settings.MEDIA_ROOT, 'foods')
        media_categories_dir = os.path.join(settings.MEDIA_ROOT, 'categories')
        os.makedirs(media_foods_dir, exist_ok=True)
        os.makedirs(media_categories_dir, exist_ok=True)

        # Helper to copy image from static to media
        def get_media_image(filename):
            static_path = os.path.join(settings.BASE_DIR, 'static', filename)
            dest_path = os.path.join(media_foods_dir, filename)
            if os.path.exists(static_path):
                if not os.path.exists(dest_path):
                    shutil.copy(static_path, dest_path)
                return f"foods/{filename}"
            return ""

        # Map categories to static images
        image_mapping = {
            'Burgers': 'veg-burger.jpg',
            'Wraps': 'paneer-wrap.jpg',
            'Pizza': 'veg-pizza.jpg',
            'South Indian': 'Dosa.jpg',
            'Snacks': 'Samosa.jpg',
            'Sandwich': 'paneer-wrap.jpg',
            'Fast Food': 'veg-burger.jpg',
            'Chinese': 'veg-pizza.jpg',
            'Beverages': 'Dabeli.jpg',
            'Desserts': 'Dabeli.jpg'
        }

        # Categories list
        categories_data = [
            'Burgers', 'Wraps', 'Pizza', 'South Indian', 'Snacks',
            'Chinese', 'Sandwich', 'Fast Food', 'Beverages', 'Desserts'
        ]

        categories = {}
        for name in categories_data:
            img_file = image_mapping.get(name, '')
            media_rel_path = ""
            if img_file:
                # Copy to categories folder too for neatness
                cat_static_path = os.path.join(settings.BASE_DIR, 'static', img_file)
                cat_dest_path = os.path.join(media_categories_dir, img_file)
                if os.path.exists(cat_static_path):
                    if not os.path.exists(cat_dest_path):
                        shutil.copy(cat_static_path, cat_dest_path)
                    media_rel_path = f"categories/{img_file}"

            cat, created = Category.objects.get_or_create(
                name=name,
                defaults={'image': media_rel_path}
            )
            categories[name] = cat
            self.stdout.write(f"Category '{name}': {'Created' if created else 'Already Exists'}")

        # Food items list
        food_items_data = [
            # 1. Burgers
            ('Veg Burger', 'Burgers', 'Crispy mixed vegetable patty topped with fresh lettuce, onions, tomato, and creamy burger sauce in a soft toasted bun.', 99.00, 'veg-burger.jpg'),
            ('Cheese Burger', 'Burgers', 'Classic vegetable patty with a melting slice of cheddar cheese, fresh toppings, and house mayo.', 119.00, 'veg-burger.jpg'),
            ('Paneer Burger', 'Burgers', 'Soft burger bun filled with crispy paneer patty, fresh vegetables and creamy sauce.', 149.00, 'veg-burger.jpg'),
            ('Aloo Tikki Burger', 'Burgers', 'Our value special burger containing a golden-fried spiced potato patty, onion rings, and sweet-spicy sauces.', 79.00, 'veg-burger.jpg'),
            ('Double Cheese Burger', 'Burgers', 'Juicy double vegetable patty, layered with double slices of cheese, pickles, and our signature burger dressing.', 169.00, 'veg-burger.jpg'),

            # 2. Wraps
            ('Paneer Wrap', 'Wraps', 'Toasted tortilla wrap stuffed with spiced cottage cheese cubes, bell peppers, crunchy onions, and mint chutney.', 139.00, 'paneer-wrap.jpg'),
            ('Veg Wrap', 'Wraps', 'Flour wrap loaded with sauteed fresh vegetables, potato bites, green chutney, and mild spices.', 109.00, 'paneer-wrap.jpg'),
            ('Cheese Paneer Wrap', 'Wraps', 'Cottage cheese chunks combined with melted mozzarella cheese, grilled bell peppers, and creamy mayonnaise in a wrap.', 159.00, 'paneer-wrap.jpg'),
            ('Mexican Veg Wrap', 'Wraps', 'Spiced beans, sweet corn, salsa, crispy greens, and a hint of jalapeno sauce wrapped in a soft tortilla.', 129.00, 'paneer-wrap.jpg'),
            ('Spicy Paneer Wrap', 'Wraps', 'Crispy fried paneer fingers tossed in a hot Schezwan glaze, wrapped with crunchy vegetables and spicy mayo.', 149.00, 'paneer-wrap.jpg'),

            # 3. Pizza
            ('Veg Pizza', 'Pizza', 'Fresh hand-tossed dough loaded with tomato sauce, mozzarella, bell peppers, onions, tomatoes, and mushrooms.', 199.00, 'veg-pizza.jpg'),
            ('Paneer Pizza', 'Pizza', 'Indian fusion pizza topped with marinated paneer tikka cubes, capsicum, red onions, and hot green chillies.', 249.00, 'veg-pizza.jpg'),
            ('Margherita Pizza', 'Pizza', 'Simplicity at its best - rich herb tomato sauce topped with gooey mozzarella cheese and fresh basil leaves.', 179.00, 'veg-pizza.jpg'),
            ('Cheese Corn Pizza', 'Pizza', 'Delicious golden sweet corn kernels paired with extra mozzarella cheese on a crispy crust.', 219.00, 'veg-pizza.jpg'),
            ('Farmhouse Pizza', 'Pizza', 'Loaded pizza topped with mushrooms, sweet corn, tomatoes, capsicum, red onions, and black olives.', 269.00, 'veg-pizza.jpg'),

            # 4. South Indian
            ('Plain Dosa', 'South Indian', 'Thin, golden, crispy crepe made from fermented rice and lentil batter, served with coconut chutney and hot sambar.', 79.00, 'Dosa.jpg'),
            ('Masala Dosa', 'South Indian', 'Crispy rice crepe filled with a savory spiced mashed potato masala filling, served with sambar and chutney.', 99.00, 'Dosa.jpg'),
            ('Cheese Dosa', 'South Indian', 'Crispy dosa layered with shredded mozzarella cheese, green chillies, and butter.', 129.00, 'Dosa.jpg'),
            ('Paneer Dosa', 'South Indian', 'Golden crepe filled with a tasty filling of grated paneer, onions, tomatoes, and green coriander.', 139.00, 'Dosa.jpg'),
            ('Idli', 'South Indian', 'Three pieces of soft, fluffy steamed rice cakes served with traditional coconut chutney and rich vegetable sambar.', 59.00, 'Dosa.jpg'),
            ('Medu Vada', 'South Indian', 'Two pieces of crispy, deep-fried savory lentil doughnuts served hot with sambar and fresh chutney.', 69.00, 'Dosa.jpg'),
            ('Uttapam', 'South Indian', 'Thick savory pancake topped with finely chopped onions, tomatoes, capsicum, and green chillies.', 89.00, 'Dosa.jpg'),

            # 5. Snacks
            ('Samosa', 'Snacks', 'Golden pastry crust filled with spiced potatoes and green peas, served with sweet tamarind chutney.', 20.00, 'Samosa.jpg'),
            ('Dabeli', 'Snacks', 'Spicy potato filling inside a soft burger bun, garnished with pomegranate seeds, peanuts, and sev.', 30.00, 'Dabeli.jpg'),
            ('Vada Pav', 'Snacks', 'The classic Mumbai street food - batata vada inside a pav bun, layered with dry garlic chutney and green chillies.', 25.00, 'Samosa.jpg'),
            ('Kachori', 'Snacks', 'Crispy flaky shell filled with a mixture of spiced lentils or onions, served with tangy chutney.', 25.00, 'Samosa.jpg'),
            ('Frankie', 'Snacks', 'Warm flatbread rolled with a spicy potato mash, onions, chat masala, and a tangy vinegar dressing.', 89.00, 'paneer-wrap.jpg'),
            ('Aloo Samosa', 'Snacks', 'Crispy triangular pastry stuffed with highly seasoned mashed potatoes and toasted spices.', 30.00, 'Samosa.jpg'),
            ('Paneer Samosa', 'Snacks', 'Delicious variant of samosa filled with spiced paneer crumbs, coriander, and mild herbs.', 45.00, 'Samosa.jpg'),

            # 6. Chinese
            ('Veg Manchurian', 'Chinese', 'Deep-fried mixed vegetable balls cooked in a rich, tangy, and slightly sweet soya-garlic gravy.', 129.00, 'veg-pizza.jpg'),
            ('Veg Hakka Noodles', 'Chinese', 'Stir-fried wheat noodles tossed with julienned vegetables, white pepper, and light soy sauce.', 119.00, 'veg-pizza.jpg'),
            ('Veg Fried Rice', 'Chinese', 'Wok-tossed steamed rice cooked with finely diced carrots, beans, spring onions, and a splash of soy sauce.', 119.00, 'veg-pizza.jpg'),
            ('Schezwan Noodles', 'Chinese', 'Spicy stir-fried noodles cooked with red hot Schezwan sauce, garlic, and fresh vegetables.', 139.00, 'veg-pizza.jpg'),
            ('Chilli Paneer', 'Chinese', 'Wok-tossed paneer cubes with bell peppers, onions, ginger, and green chillies in a spicy soy-chilli glaze.', 159.00, 'veg-pizza.jpg'),

            # 7. Sandwich
            ('Veg Sandwich', 'Sandwich', 'Fresh bread slices layered with sliced cucumber, tomatoes, potatoes, onions, and spicy green coriander chutney.', 59.00, 'paneer-wrap.jpg'),
            ('Cheese Sandwich', 'Sandwich', 'Simple yet delicious toasted sandwich stuffed with loaded cheddar and mozzarella cheese.', 79.00, 'paneer-wrap.jpg'),
            ('Grilled Sandwich', 'Sandwich', 'Double decker bread filled with spiced vegetables, cheese, and grilled golden brown with butter.', 99.00, 'paneer-wrap.jpg'),
            ('Paneer Sandwich', 'Sandwich', 'Toasted sandwich stuffed with seasoned paneer bhurji, fresh capsicum, and mint mayonnaise.', 109.00, 'paneer-wrap.jpg'),
            ('Cheese Corn Sandwich', 'Sandwich', 'Sweet corn kernels mixed with creamy cheese spread and grilled between two slices of buttered bread.', 89.00, 'paneer-wrap.jpg'),

            # 8. Fast Food
            ('French Fries', 'Fast Food', 'Golden fried potato strips, lightly salted and served crispy with tomato ketchup.', 79.00, 'veg-burger.jpg'),
            ('Peri Peri Fries', 'Fast Food', 'Crisp potato fries tossed in a spicy, tangy, and aromatic African peri-peri seasoning.', 89.00, 'veg-burger.jpg'),
            ('Cheese Fries', 'Fast Food', 'Golden potato fries drenched in a hot, creamy, and gooey cheese sauce.', 119.00, 'veg-burger.jpg'),
            ('Garlic Bread', 'Fast Food', 'Four pieces of toasted baguette slices brushed with garlic butter, parsley, and melted mozzarella.', 99.00, 'veg-burger.jpg'),
            ('Loaded Fries', 'Fast Food', 'Crisp fries topped with cheese sauce, chopped onions, tomatoes, jalapenos, and signature burger dressing.', 139.00, 'veg-burger.jpg'),

            # 9. Beverages
            ('Cold Coffee', 'Beverages', 'Thick, creamy, and refreshing blended coffee served chilled with a scoop of vanilla ice cream.', 79.00, 'Dabeli.jpg'),
            ('Masala Chaas', 'Beverages', 'Refreshing buttermilk seasoned with black salt, cumin powder, ginger, green coriander, and mint.', 39.00, 'Dabeli.jpg'),
            ('Lemon Soda', 'Beverages', 'Chilled soda water mixed with fresh lime juice, sugar, salt, and spices, served sweet or salted.', 49.00, 'Dabeli.jpg'),
            ('Fresh Lime Water', 'Beverages', 'Classic refreshing homemade lime drink made with chilled water, lemon juice, sugar, and a pinch of salt.', 39.00, 'Dabeli.jpg'),
            ('Soft Drink', 'Beverages', 'Assorted 300ml carbonated soft drinks served chilled (Cola, Lime, Orange).', 29.00, 'Dabeli.jpg'),

            # 10. Desserts
            ('Gulab Jamun', 'Desserts', 'Two pieces of warm, soft milk-solid dumplings fried and soaked in cardamom-flavored sugar syrup.', 49.00, 'Dabeli.jpg'),
            ('Brownie', 'Desserts', 'Rich, fudgy chocolate brownie served warm, perfect as is or with vanilla ice cream.', 89.00, 'Dabeli.jpg'),
            ('Vanilla Ice Cream', 'Desserts', 'Classic creamy vanilla bean ice cream scoop served with a drizzle of chocolate sauce.', 49.00, 'Dabeli.jpg'),
            ('Chocolate Ice Cream', 'Desserts', 'Rich double chocolate ice cream scoop topped with chocolate chips and chocolate syrup.', 59.00, 'Dabeli.jpg'),
            ('Gajar Halwa', 'Desserts', 'Traditional Indian sweet pudding made with fresh grated carrots, milk, ghee, sugar, and loaded with dry fruits.', 79.00, 'Dabeli.jpg'),
        ]

        import random
        for name, category_name, desc, price, img_file in food_items_data:
            cat = categories[category_name]
            rel_image_path = get_media_image(img_file)
            
            # Apply discounts to some featured items
            dec_price = Decimal(str(price))
            discount = None
            if price > 100 and random.choice([True, False]):
                discount = Decimal(str(round(price * 0.85, 2))) # 15% off
            
            stock_qty = random.randint(15, 80)

            food, created = FoodItem.objects.update_or_create(
                name=name,
                category=cat,
                defaults={
                    'description': desc,
                    'price': dec_price,
                    'discount_price': discount,
                    'stock': stock_qty,
                    'image': rel_image_path,
                    'is_available': True
                }
            )
            # Ensure slug is generated
            food.save()
            self.stdout.write(f"FoodItem '{name}': {'Created' if created else 'Updated'}")

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))

