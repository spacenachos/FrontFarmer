
import time
import random

class Tool:
    def __init__(self, name, cost, multiplier, description):
        self.name = name
        self.cost = cost
        self.multiplier = multiplier
        self.description = description

class Seed:
    def __init__(self, name, cost, growth_time, sell_price, rarity="common", plant_type="plant", toolkit_req=None, fertilizer_req=None):
        self.name = name
        self.cost = cost
        self.growth_time = growth_time
        self.sell_price = sell_price
        self.rarity = rarity
        self.plant_type = plant_type  # "flower", "plant", "tree"
        self.toolkit_req = toolkit_req
        self.fertilizer_req = fertilizer_req

class Crop:
    def __init__(self, name, growth_time, sell_price, rarity="common", plant_type="plant"):
        self.name = name
        self.growth_time = growth_time
        self.growth_progress = 0
        self.sell_price = sell_price
        self.is_ready = False
        self.rarity = rarity
        self.plant_type = plant_type
        self.last_watered = 0
        self.needs_watering = plant_type in ["tree"]
        self.water_interval = 10 if plant_type == "tree" else 15
        self.quirks = self._get_quirks(name)
        self.pest_resistance = self._get_pest_resistance(name)
        self.attracts_beneficial = self._get_beneficial_attraction(name)
        
    def _get_quirks(self, name):
        quirks = {
            "Ash Tree": "Needs extremely moist soil to survive",
            "Aspen Tree": "Grows fast and cannot be affected by pests", 
            "Beech Tree": "Can attract butterflies/honeybees for flowers, very weak to pests",
            "Willow Tree": "Takes 3 hours to grow, but has the best payout of any tree",
            "Rose": "Hardest flower to cultivate, hard to sell with thorns but fast growing time"
        }
        return quirks.get(name, "")
    
    def _get_pest_resistance(self, name):
        if name == "Aspen Tree":
            return "immune"
        elif name == "Beech Tree":
            return "very_weak"
        else:
            return "normal"
    
    def _get_beneficial_attraction(self, name):
        if name == "Beech Tree":
            return ["butterflies", "honeybees"]
        return []

class Fertilizer:
    def __init__(self, level, cost, boost, description):
        self.level = level
        self.cost = cost
        self.boost = boost
        self.description = description

class Shed:
    def __init__(self, name, cost, flower_pots, plant_pots, tree_plots, description):
        self.name = name
        self.cost = cost
        self.flower_pots = flower_pots
        self.plant_pots = plant_pots
        self.tree_plots = tree_plots
        self.description = description

class Polytechnic:
    def __init__(self, name, max_level, cost_per_level, description):
        self.name = name
        self.max_level = max_level
        self.current_level = 0
        self.cost_per_level = cost_per_level
        self.description = description

class Lab:
    def __init__(self):
        self.owned = False
        self.cost = 2500
        self.recipes = {
            "Apple Tree": "Apple Pie",
            "Wheat": "Bread",
            "Tomato": "Tomato Sauce",
            "Grape": "Wine",
            "Strawberry": "Strawberry Jam",
            "Rose": "Rose Perfume",
            "Lavender": "Lavender Oil",
            "Ash Tree": "Ash Wood",
            "Oak Tree": "Oak Wood",
            "Maple Tree": "Maple Syrup",
            "Willow Tree": "Premium Willow Wood",
            "Pine Tree": "Pine Wood",
            "Cedar Tree": "Cedar Wood",
            "Walnut Tree": "Walnut Wood"
        }

class Farm:
    def __init__(self):
        self.money = 100
        self.day = 1
        self.crops = []
        self.inventory = {}
        self.seeds = {"Wheat": 3, "Carrot": 2}
        self.tools = {
            "Basic Hoe": False,
            "Watering Can": False,
            "Fertilizer": False,
            "Premium Soil": False,
            "Growth Accelerator": False,
            "Quantum Enhancer": False,
            "Time Manipulator": False
        }
        self.fertilizers = {}
        self.experience = 0
        self.level = 1
        self.experience_to_next_level = 100
        self.max_plots = 4
        self.shed = None
        self.lab = Lab()
        self.polytechnics = {
            "Robotics": Polytechnic("Robotics", 5, [500, 1000, 2000, 4000, 8000], "Automates farming tasks"),
            "Logistics": Polytechnic("Logistics", 5, [750, 1500, 3000, 6000, 12000], "Speeds up all processes"),
            "Information": Polytechnic("Information", 5, [600, 1200, 2400, 4800, 9600], "Shows plant properties"),
            "Transportation": Polytechnic("Transportation", 5, [800, 1600, 3200, 6400, 12800], "Automates lab processes"),
            "Economics": Polytechnic("Economics", 5, [1000, 2000, 4000, 8000, 16000], "Generates passive income")
        }

    def can_upgrade_polytechnic(self, poly_name):
        poly = self.polytechnics[poly_name]
        if poly.current_level >= poly.max_level:
            return False
        
        # Check if all other polytechnics are at required level
        min_level = poly.current_level
        for other_name, other_poly in self.polytechnics.items():
            if other_name != poly_name and other_poly.current_level < min_level:
                return False
        return True

    def upgrade_polytechnic(self, poly_name):
        poly = self.polytechnics[poly_name]
        if not self.can_upgrade_polytechnic(poly_name):
            return False
        
        cost = poly.cost_per_level[poly.current_level]
        if self.money >= cost:
            self.money -= cost
            poly.current_level += 1
            return True
        return False

    def buy_shed(self, shed_type):
        sheds = {
            "Flat Home": Shed("Flat Home", 500, {"small": 4, "medium": 2, "large": 1}, {"small": 0, "medium": 0, "large": 0}, {"small": 0, "medium": 0, "large": 0}, "Basic flower growing"),
            "Modern Barn": Shed("Modern Barn", 1500, {"small": 8, "medium": 4, "large": 2}, {"small": 8, "medium": 4, "large": 2}, {"small": 0, "medium": 0, "large": 0}, "Flowers and plants"),
            "Science Lab": Shed("Science Lab", 5000, {"small": 8, "medium": 4, "large": 2}, {"small": 8, "medium": 4, "large": 2}, {"small": 0, "medium": 0, "large": 0}, "Includes lab access"),
            "Biosphere": Shed("Biosphere", 15000, {"small": 16, "medium": 8, "large": 4}, {"small": 16, "medium": 8, "large": 4}, {"small": 16, "medium": 8, "large": 4}, "Full farming complex")
        }
        
        if shed_type in sheds and self.money >= sheds[shed_type].cost:
            self.money -= sheds[shed_type].cost
            self.shed = sheds[shed_type]
            if shed_type in ["Science Lab", "Biosphere"]:
                self.lab.owned = True
            self.update_max_plots()
            return True
        return False

    def update_max_plots(self):
        if self.shed:
            total_plots = 0
            for size, count in self.shed.flower_pots.items():
                total_plots += count
            for size, count in self.shed.plant_pots.items():
                total_plots += count
            for size, count in self.shed.tree_plots.items():
                total_plots += count
            self.max_plots = total_plots
        else:
            self.max_plots = 4

    def water_crop(self, crop_index):
        if 0 <= crop_index < len(self.crops):
            crop = self.crops[crop_index]
            if crop.needs_watering and (self.day - crop.last_watered) >= crop.water_interval / (24 * 60):  # Convert minutes to days
                crop.last_watered = self.day
                return True
        return False

    def crossbreed_plants(self, crop1_index, crop2_index):
        if not self.lab.owned:
            return None
        
        if 0 <= crop1_index < len(self.crops) and 0 <= crop2_index < len(self.crops):
            crop1 = self.crops[crop1_index]
            crop2 = self.crops[crop2_index]
            
            if crop1.plant_type == crop2.plant_type and crop1.is_ready and crop2.is_ready:
                # Create hybrid with combined traits
                hybrid_name = f"{crop1.name}-{crop2.name} Hybrid"
                hybrid_price = int((crop1.sell_price + crop2.sell_price) * 1.5)
                return hybrid_name, hybrid_price
        return None

    def refine_material(self, crop_name):
        if not self.lab.owned:
            return False
        
        if crop_name in self.lab.recipes and crop_name in self.inventory:
            refined = self.lab.recipes[crop_name]
            self.inventory[crop_name] -= 1
            if self.inventory[crop_name] <= 0:
                del self.inventory[crop_name]
            
            if refined not in self.inventory:
                self.inventory[refined] = 0
            self.inventory[refined] += 1
            return True
        return False

    def plant_seed(self, seed_name):
        if len(self.crops) >= self.max_plots:
            return False
            
        if seed_name in self.seeds and self.seeds[seed_name] > 0:
            # Get seed info from shop
            shop = Shop()
            if seed_name in shop.seeds_for_sale:
                seed_info = shop.seeds_for_sale[seed_name]
                
                # Check toolkit requirements
                if seed_info.toolkit_req and not self.tools.get(seed_info.toolkit_req, False):
                    return False
                
                # Check fertilizer requirements
                if seed_info.fertilizer_req and seed_info.fertilizer_req not in self.fertilizers:
                    return False
                
                crop = Crop(seed_name, seed_info.growth_time, seed_info.sell_price, seed_info.rarity, seed_info.plant_type)
                self.crops.append(crop)
                self.seeds[seed_name] -= 1
                self.add_experience(5)
                return True
        return False

    def grow_crops(self, weather):
        weather_changed = weather.update_weather()
        if weather_changed:
            print(f"\n🌤️ Weather changed! {weather.get_current_weather_info()}")
        
        growth_modifier = weather.get_growth_modifier()
        
        # Apply tool multipliers
        tool_multiplier = 1.0
        for tool_name, owned in self.tools.items():
            if owned:
                tool_info = Shop.get_tool_by_name(tool_name)
                if tool_info:
                    tool_multiplier *= tool_info.multiplier
        
        # Apply polytechnic bonuses
        logistics_bonus = 1.0 + (self.polytechnics["Logistics"].current_level * 0.1)
        
        for crop in self.crops:
            if not crop.is_ready:
                # Check watering penalty
                watering_penalty = 1.0
                if crop.needs_watering and (self.day - crop.last_watered) > (crop.water_interval / (24 * 60)):
                    watering_penalty = 0.5  # Slower growth if not watered
                
                growth_amount = growth_modifier * tool_multiplier * logistics_bonus * watering_penalty
                crop.growth_progress += growth_amount
                
                if crop.growth_progress >= crop.growth_time:
                    crop.is_ready = True
                    
                    # Weather rarity boost
                    rarity_boost = weather.get_rarity_boost()
                    if random.random() < (0.1 * rarity_boost):
                        if crop.rarity == "common":
                            crop.rarity = "rare"
                            crop.name = f"Rare {crop.name}"
                            crop.sell_price *= 3
                        elif crop.rarity == "rare":
                            crop.rarity = "epic"
                            crop.name = f"Epic {crop.name}"
                            crop.sell_price *= 2
        
        self.day += 1
        self.add_experience(2)
        
        # Economics passive income
        economics_income = self.polytechnics["Economics"].current_level * 10
        if economics_income > 0:
            self.money += economics_income
            print(f"💰 Economics generated ${economics_income}!")

    def harvest_crop(self, crop_index):
        if 0 <= crop_index < len(self.crops):
            crop = self.crops[crop_index]
            if crop.is_ready:
                if crop.name not in self.inventory:
                    self.inventory[crop.name] = 0
                self.inventory[crop.name] += 1
                self.crops.pop(crop_index)
                self.add_experience(10)
                return True
        return False

    def sell_crop(self, crop_name, amount):
        if crop_name in self.inventory and self.inventory[crop_name] >= amount:
            shop = Shop()
            if crop_name in shop.crop_prices:
                total_price = shop.crop_prices[crop_name] * amount
                self.money += total_price
                self.inventory[crop_name] -= amount
                if self.inventory[crop_name] == 0:
                    del self.inventory[crop_name]
                self.add_experience(amount * 2)
                return total_price
        return 0

    def add_experience(self, amount):
        self.experience += amount
        while self.experience >= self.experience_to_next_level:
            self.experience -= self.experience_to_next_level
            self.level += 1
            self.experience_to_next_level = int(self.experience_to_next_level * 1.5)
            
            reward_money = self.level * 50
            self.money += reward_money
            
            if self.level % 5 == 0:
                self.max_plots += 2
            
            print(f"🎉 Level up! You're now level {self.level}!")
            print(f"💰 Bonus: ${reward_money}")
            if self.level % 5 == 0:
                print(f"🏡 Farm expanded! +2 plots (Total: {self.max_plots})")

    def display_inventory(self):
        print("\n--- Inventory ---")
        print(f"Day: {self.day} | Money: ${self.money}")
        print(f"Level: {self.level} | XP: {self.experience}/{self.experience_to_next_level}")
        
        if self.shed:
            print(f"Shed: {self.shed.name}")
        if self.lab.owned:
            print("Lab: Available")
        
        print("Tools:")
        if not any(self.tools.values()):
            print("  No tools")
        else:
            for tool_name, owned in self.tools.items():
                if owned:
                    print(f"  {tool_name}")
        
        print("Fertilizers:")
        if not self.fertilizers:
            print("  No fertilizers")
        else:
            for fert_name, count in self.fertilizers.items():
                print(f"  {fert_name}: {count}")
        
        print("Seeds:")
        if not self.seeds or all(count == 0 for count in self.seeds.values()):
            print("  No seeds")
        else:
            for seed_name, count in self.seeds.items():
                if count > 0:
                    print(f"  {seed_name}: {count}")
        
        print("Harvested crops:")
        if not self.inventory:
            print("  No harvested crops")
        else:
            for crop_name, count in self.inventory.items():
                print(f"  {crop_name}: {count}")

    def display_crops(self):
        print("\n--- Your Farm ---")
        if not self.crops:
            print("No crops planted.")
        else:
            for i, crop in enumerate(self.crops):
                if crop.is_ready:
                    status = "Ready"
                else:
                    progress = min(100, int((crop.growth_progress / crop.growth_time) * 100))
                    status = f"Growing ({progress}%)"
                
                water_status = ""
                if crop.needs_watering:
                    time_since_water = self.day - crop.last_watered
                    if time_since_water > (crop.water_interval / (24 * 60)):
                        water_status = " 💧NEEDS WATER"
                
                rarity_indicator = f" ({crop.rarity.upper()})" if crop.rarity != "common" else ""
                print(f"{i + 1}. {crop.name}{rarity_indicator} ({status}){water_status}")
        print(f"Plots used: {len(self.crops)}/{self.max_plots}")

class Weather:
    def __init__(self):
        self.current_weather = "sunny"
        self.weather_types = {
            "sunny": {"growth_modifier": 1.0, "rarity_boost": 1.0, "description": "Perfect growing conditions!"},
            "rainy": {"growth_modifier": 0.8, "rarity_boost": 1.3, "description": "Rain helps rare crops grow!"},
            "cloudy": {"growth_modifier": 0.9, "rarity_boost": 1.1, "description": "Mild conditions."},
            "stormy": {"growth_modifier": 1.2, "rarity_boost": 0.8, "description": "Dangerous but fast growth!"},
            "drought": {"growth_modifier": 1.5, "rarity_boost": 0.6, "description": "Harsh conditions, fast but poor quality."},
            "magical_mist": {"growth_modifier": 0.5, "rarity_boost": 2.5, "description": "Mystical weather enhances rare crops!"}
        }
        self.days_until_change = random.randint(3, 7)
    
    def update_weather(self):
        self.days_until_change -= 1
        if self.days_until_change <= 0:
            old_weather = self.current_weather
            self.current_weather = random.choice(list(self.weather_types.keys()))
            self.days_until_change = random.randint(3, 7)
            if old_weather != self.current_weather:
                return True
        return False
    
    def get_current_weather_info(self):
        weather_data = self.weather_types[self.current_weather]
        return f"Weather: {self.current_weather.replace('_', ' ').title()} - {weather_data['description']}"
    
    def get_growth_modifier(self):
        return self.weather_types[self.current_weather]["growth_modifier"]
    
    def get_rarity_boost(self):
        return self.weather_types[self.current_weather]["rarity_boost"]

class Shop:
    def __init__(self):
        self.seeds_for_sale = self._generate_all_seeds()
        self.tools_for_sale = self._generate_tools()
        self.fertilizers_for_sale = self._generate_fertilizers()
        self.crop_prices = self._generate_crop_prices()
        self.stock = self._initialize_stock()
        self.last_restock = 0
        
    def _generate_fertilizers(self):
        return {
            "Fertilizer I": Fertilizer(1, 20, 1.2, "Basic fertilizer, 20% growth boost"),
            "Fertilizer II": Fertilizer(2, 50, 1.4, "Improved fertilizer, 40% growth boost"),
            "Fertilizer III": Fertilizer(3, 100, 1.6, "Advanced fertilizer, 60% growth boost"),
            "Fertilizer IV": Fertilizer(4, 200, 1.8, "Premium fertilizer, 80% growth boost"),
            "Fertilizer V": Fertilizer(5, 400, 2.0, "Ultimate fertilizer, 100% growth boost")
        }
        
    def _generate_all_seeds(self):
        seeds = {}
        
        # Flowers (no toolkit, fertilizer up to III)
        flowers = [
            ("Sunflower", 15, 8, 25, "common"), ("Marigold", 8, 5, 12, "common"), ("Petunia", 6, 4, 9, "common"),
            ("Rose", 45, 8, 75, "rare"), ("Orchid", 35, 15, 60, "epic"), ("Golden Rose", 100, 25, 180, "legendary"),
            ("Tulip", 12, 6, 18, "common"), ("Daffodil", 10, 5, 15, "common"), ("Lily", 18, 8, 30, "rare"),
            ("Violet", 14, 7, 22, "common"), ("Jasmine", 25, 12, 45, "rare"), ("Lotus", 50, 20, 90, "epic"),
            ("Iris", 16, 8, 28, "common"), ("Carnation", 13, 6, 20, "common"), ("Chrysanthemum", 22, 10, 38, "rare"),
            ("Peony", 28, 14, 50, "rare"), ("Hibiscus", 20, 10, 35, "common"), ("Azalea", 30, 15, 55, "rare"),
            ("Begonia", 15, 7, 25, "common"), ("Camellia", 45, 18, 80, "epic"),
            # New flowers from specifications
            ("Lavender", 18, 9, 32, "common"), ("Daisy", 8, 4, 12, "common"),
            ("Hydrangea", 25, 12, 45, "rare"), ("Yarrow", 12, 6, 18, "common"),
            ("Dahlia", 20, 10, 35, "rare"), ("Gardenia", 35, 16, 65, "epic")
        ]
        
        for name, cost, growth_time, sell_price, rarity in flowers:
            # Special case for Rose which requires Fertilizer III despite being rare
            if name == "Rose":
                fert_req = "Fertilizer III"
            else:
                fert_req = None if rarity == "common" else "Fertilizer II" if rarity == "rare" else "Fertilizer III"
            seeds[name] = Seed(name, cost, growth_time, sell_price, rarity, "flower", None, fert_req)
        
        # Plants (basic toolkit, fertilizer I-IV)
        plants = [
            ("Wheat", 5, 3, 8, "common"), ("Corn", 8, 4, 12, "common"), ("Carrot", 3, 2, 6, "common"),
            ("Potato", 6, 5, 15, "common"), ("Tomato", 10, 6, 20, "common"), ("Lettuce", 4, 2, 5, "common"),
            ("Spinach", 7, 4, 9, "common"), ("Broccoli", 12, 6, 18, "rare"), ("Cauliflower", 15, 7, 22, "rare"),
            ("Asparagus", 18, 8, 28, "rare"), ("Artichoke", 25, 10, 40, "epic"), ("Truffle Mushroom", 80, 15, 150, "legendary"),
            ("Cabbage", 8, 4, 12, "common"), ("Onion", 6, 3, 9, "common"), ("Garlic", 7, 4, 11, "common"),
            ("Pepper", 9, 5, 14, "common"), ("Cucumber", 8, 4, 12, "common"), ("Zucchini", 10, 5, 16, "common"),
            ("Eggplant", 12, 6, 18, "rare"), ("Pumpkin", 20, 8, 32, "rare")
        ]
        
        for name, cost, growth_time, sell_price, rarity in plants:
            toolkit = "Basic Hoe"
            fert_levels = {"common": "Fertilizer I", "rare": "Fertilizer II", "epic": "Fertilizer III", "legendary": "Fertilizer IV"}
            seeds[name] = Seed(name, cost, growth_time, sell_price, rarity, "plant", toolkit, fert_levels[rarity])
        
        # Trees (advanced toolkit, fertilizer II-V)
        trees = [
            ("Apple Tree", 30, 15, 50, "common"), ("Pear", 28, 14, 45, "common"), ("Cherry Tree", 35, 16, 60, "rare"),
            ("Plum", 32, 15, 55, "rare"), ("Peach", 38, 17, 65, "rare"), ("Orange", 40, 18, 70, "rare"),
            ("Lemon", 35, 16, 60, "rare"), ("Olive", 50, 20, 90, "epic"), ("Avocado", 60, 22, 110, "epic"),
            ("Mango", 70, 25, 130, "epic"), ("Dragon Fruit Tree", 150, 35, 280, "legendary"), ("Money Tree", 500, 50, 1000, "legendary"),
            ("Oak Tree", 45, 20, 80, "common"), ("Maple Tree", 50, 22, 90, "rare"), ("Pine Tree", 40, 18, 70, "common"),
            ("Willow Tree", 120, 120, 300, "epic"), ("Birch Tree", 42, 19, 75, "common"), ("Cedar Tree", 60, 24, 110, "epic"),
            ("Redwood", 100, 30, 200, "epic"), ("Ancient Tree", 300, 45, 600, "legendary"),
            # New trees from specifications
            ("Ash Tree", 35, 18, 65, "common"), ("Aspen Tree", 25, 12, 45, "common"), 
            ("Beech Tree", 55, 20, 85, "rare"), ("Elm Tree", 40, 16, 70, "common"),
            ("Eucalyptus Tree", 65, 25, 110, "rare"), ("Fir Tree", 38, 17, 68, "common"),
            ("Hemlock Tree", 45, 19, 78, "rare"), ("Hickory Tree", 50, 21, 88, "rare"),
            ("Mangrove Tree", 70, 28, 125, "epic"), ("Spruce Tree", 35, 16, 62, "common"),
            ("Sycamore Tree", 48, 20, 82, "rare"), ("Walnut Tree", 75, 30, 140, "epic")
        ]
        
        for name, cost, growth_time, sell_price, rarity in trees:
            toolkit = "Premium Soil"  # Advanced toolkit requirement
            fert_levels = {"common": "Fertilizer II", "rare": "Fertilizer III", "epic": "Fertilizer IV", "legendary": "Fertilizer V"}
            
            # Special fertilizer requirements based on specifications
            if name == "Ash Tree":
                fert_req = "Fertilizer III"
            elif name == "Aspen Tree":
                fert_req = "Fertilizer II"
            elif name == "Beech Tree":
                fert_req = "Fertilizer V"
            elif name == "Willow Tree":
                fert_req = "Fertilizer IV"
            else:
                fert_req = fert_levels[rarity]
            
            seeds[name] = Seed(name, cost, growth_time, sell_price, rarity, "tree", toolkit, fert_req)
        
        return seeds
    
    def _generate_tools(self):
        return {
            "Basic Hoe": Tool("Basic Hoe", 50, 0.9, "Basic toolkit for plants - Reduces growth time by 10%"),
            "Watering Can": Tool("Watering Can", 75, 0.95, "Helps with watering - Reduces growth time by 5%"),
            "Fertilizer": Tool("Fertilizer", 100, 0.8, "Speeds growth - Reduces growth time by 20%"),
            "Premium Soil": Tool("Premium Soil", 200, 0.7, "Advanced toolkit for trees - Reduces growth time by 30%"),
            "Growth Accelerator": Tool("Growth Accelerator", 500, 0.5, "Reduces growth time by 50%"),
            "Quantum Enhancer": Tool("Quantum Enhancer", 1000, 0.3, "Reduces growth time by 70%"),
            "Time Manipulator": Tool("Time Manipulator", 2500, 0.1, "Reduces growth time by 90%")
        }
    
    def _generate_crop_prices(self):
        prices = {}
        for seed_name, seed in self.seeds_for_sale.items():
            base_price = max(1, seed.cost // 3)
            if seed.rarity == "rare":
                base_price *= 3
            elif seed.rarity == "epic":
                base_price *= 6
            elif seed.rarity == "legendary":
                base_price *= 12
            prices[seed_name] = base_price
        return prices
    
    def _initialize_stock(self):
        stock = {}
        for seed_name, seed in self.seeds_for_sale.items():
            if seed.rarity == "common":
                stock[seed_name] = random.randint(5, 20)
            elif seed.rarity == "rare":
                stock[seed_name] = random.randint(1, 5)
            elif seed.rarity == "epic":
                stock[seed_name] = random.randint(0, 3)
            elif seed.rarity == "legendary":
                stock[seed_name] = random.randint(0, 1)
        return stock
    
    def restock_shop(self):
        self.last_restock += 1
        if self.last_restock >= 10:  # Restock every 10 game actions (approximately 10 minutes)
            self.stock = self._initialize_stock()
            self.last_restock = 0
            print("🏪 Traders have restocked their inventory!")
    
    def buy_seed(self, seed_name, farm):
        if seed_name in self.seeds_for_sale and self.stock.get(seed_name, 0) > 0:
            seed = self.seeds_for_sale[seed_name]
            if farm.money >= seed.cost:
                farm.money -= seed.cost
                if seed_name not in farm.seeds:
                    farm.seeds[seed_name] = 0
                farm.seeds[seed_name] += 1
                self.stock[seed_name] -= 1
                farm.add_experience(1)
                return True
        return False
    
    def buy_tool(self, tool_name, farm):
        if tool_name in self.tools_for_sale and not farm.tools.get(tool_name, False):
            tool = self.tools_for_sale[tool_name]
            if farm.money >= tool.cost:
                farm.money -= tool.cost
                farm.tools[tool_name] = True
                farm.add_experience(5)
                return True
        return False
    
    def buy_fertilizer(self, fert_name, farm):
        if fert_name in self.fertilizers_for_sale:
            fert = self.fertilizers_for_sale[fert_name]
            if farm.money >= fert.cost:
                farm.money -= fert.cost
                if fert_name not in farm.fertilizers:
                    farm.fertilizers[fert_name] = 0
                farm.fertilizers[fert_name] += 1
                return True
        return False
    
    def sell_crop_to_shop(self, crop_name, amount, farm):
        if crop_name in farm.inventory and farm.inventory[crop_name] >= amount:
            if crop_name in self.crop_prices:
                total_price = self.crop_prices[crop_name] * amount
                farm.money += total_price
                farm.inventory[crop_name] -= amount
                if farm.inventory[crop_name] == 0:
                    del farm.inventory[crop_name]
                farm.add_experience(amount * 2)
                return total_price
        return 0

    @staticmethod
    def get_tool_by_name(tool_name):
        tools = Shop()._generate_tools()
        return tools.get(tool_name)

    def display_shop(self, filter_rarity=None, shop_type="all"):
        print("\n--- TRADING HALL ---")
        
        if shop_type in ["all", "tools"]:
            print("🔧 Tools for sale:")
            for name, tool in self.tools_for_sale.items():
                print(f"  {name} - ${tool.cost} ({tool.description})")
        
        if shop_type in ["all", "fertilizer"]:
            print("\n🌱 Fertilizers for sale:")
            for name, fert in self.fertilizers_for_sale.items():
                print(f"  {name} - ${fert.cost} ({fert.description})")
        
        if shop_type in ["all", "flowers"]:
            print("\n🌸 Flower Trader:")
            self._display_seeds_by_type("flower", filter_rarity)
        
        if shop_type in ["all", "plants"]:
            print("\n🌿 Plant Trader:")
            self._display_seeds_by_type("plant", filter_rarity)
            
        if shop_type in ["all", "trees"]:
            print("\n🌳 Tree Trader:")
            self._display_seeds_by_type("tree", filter_rarity)
        
        print("\nAvailable filters: common, rare, epic, legendary")
        print("Available traders: flowers, plants, trees, tools, fertilizer")

    def _display_seeds_by_type(self, plant_type, filter_rarity):
        displayed_count = 0
        for name, seed in self.seeds_for_sale.items():
            if seed.plant_type != plant_type:
                continue
            if filter_rarity and seed.rarity != filter_rarity:
                continue
            
            stock = self.stock.get(name, 0)
            stock_text = f"(Stock: {stock})" if stock > 0 else "(OUT OF STOCK)"
            rarity_text = f" [{seed.rarity.upper()}]" if seed.rarity != "common" else ""
            req_text = ""
            if seed.toolkit_req:
                req_text += f" Needs: {seed.toolkit_req}"
            if seed.fertilizer_req:
                req_text += f" & {seed.fertilizer_req}"
            
            if stock > 0:
                print(f"  {name}{rarity_text} - ${seed.cost} {stock_text}{req_text}")
                displayed_count += 1
                
                if displayed_count >= 10:
                    print("  ... and more! Use filters to see specific items.")
                    break

def show_introduction():
    intro_text = [
        "🏡 Welcome to the Ultimate Farming Empire! 🏡",
        "",
        "You inherit a small farm with $100 and some basic seeds.",
        "Build your farming empire by growing crops, upgrading facilities,",
        "and unlocking advanced technology!",
        "",
        "🏗️ FACILITIES:",
        "• Sheds: Flat Home → Modern Barn → Science Lab → Biosphere",
        "• Lab: Crossbreed plants and refine materials into products",
        "• Polytechnics: Unlock automation and advanced features",
        "",
        "🌱 PLANT TYPES:",
        "• Flowers: Easy to grow, make perfumes in lab",
        "• Plants: Need basic tools, become food in lab",
        "• Trees: Need advanced tools & fertilizer, highest value",
        "",
        "⚡ SPECIAL FEATURES:",
        "• Weather affects growth speed and rarity chances",
        "• Tools reduce growth time significantly",
        "• Watering keeps trees healthy",
        "• 3 specialized traders restock every 10 minutes",
        "• Polytechnic upgrades unlock automation",
        "",
        "💡 PRO TIPS:",
        "• Start with flowers (no tool requirements)",
        "• Buy sheds to expand your farming capacity",
        "• Invest in polytechnics for long-term benefits",
        "• Plan ahead - rare seeds are limited!",
        "",
        "Good luck building your farming empire! 🚜"
    ]
    
    for line in intro_text:
        print(line)
    
    print("\nPress Enter to start farming, or type 'skip' to jump right in:")
    try:
        user_input = input().strip().lower()
        return user_input != 'skip'
    except (EOFError, KeyboardInterrupt):
        print("\nSkipping to game...")
        return False

def main():
    # Show introduction
    show_intro = show_introduction()
    if not show_intro:
        print("Skipping straight to farming!\n")
    
    farm = Farm()
    shop = Shop()
    weather = Weather()
    game_running = True

    print(f"\n{weather.get_current_weather_info()}")

    while game_running:
        # Restock shop periodically
        shop.restock_shop()
        
        print("\n" + "="*60)
        print(weather.get_current_weather_info())
        farm.display_inventory()
        farm.display_crops()
        
        print("\nWhat would you like to do?")
        print("1. Plant Seeds")
        print("2. Grow Crops (Advance Day)")
        print("3. Harvest Crop")
        print("4. Visit Trading Hall")
        print("5. Buy Seeds")
        print("6. Buy Tools & Equipment")
        print("7. Sell Crops")
        print("8. Filter Traders")
        print("9. Water Crops")
        print("10. Buy/Upgrade Shed")
        print("11. Lab Operations")
        print("12. Polytechnic Upgrades")
        print("13. Quit")
        
        try:
            choice = input("Enter your choice: ").strip()
            print(f"You selected: {choice}")
            time.sleep(0.5)
        except (EOFError, KeyboardInterrupt):
            print("Input cancelled!")
            continue

        if choice == "1":
            if not farm.seeds or all(count == 0 for count in farm.seeds.values()):
                print("You have no seeds to plant!")
                continue
            
            print("Available seeds:")
            available_seeds = [name for name, count in farm.seeds.items() if count > 0]
            for i, seed_name in enumerate(available_seeds):
                count = farm.seeds[seed_name]
                print(f"{i + 1}. {seed_name} (x{count})")
            
            try:
                seed_choice = int(input("Which seed to plant? ")) - 1
                if 0 <= seed_choice < len(available_seeds):
                    seed_name = available_seeds[seed_choice]
                    if farm.plant_seed(seed_name):
                        print(f"Planted {seed_name}!")
                    else:
                        print("Cannot plant seed! Check requirements or space.")
                else:
                    print("Invalid choice!")
            except (ValueError, EOFError, KeyboardInterrupt):
                print("Invalid input!")

        elif choice == "2":
            farm.grow_crops(weather)
            print("Time passes... your crops grow!")

        elif choice == "3":
            ready_crops = [i for i, crop in enumerate(farm.crops) if crop.is_ready]
            if not ready_crops:
                print("No crops ready for harvest!")
                continue
            
            print("Ready crops:")
            for i in ready_crops:
                crop = farm.crops[i]
                print(f"{i + 1}. {crop.name}")
            
            try:
                crop_choice = int(input("Which crop to harvest? ")) - 1
                if crop_choice in ready_crops:
                    crop_name = farm.crops[crop_choice].name
                    if farm.harvest_crop(crop_choice):
                        print(f"Harvested {crop_name}!")
                    else:
                        print("Failed to harvest!")
                else:
                    print("Invalid choice or crop not ready!")
            except (ValueError, EOFError, KeyboardInterrupt):
                print("Invalid input!")

        elif choice == "4":
            shop.display_shop()

        elif choice == "5":
            print("Which trader would you like to visit?")
            print("1. Flower Trader")
            print("2. Plant Trader") 
            print("3. Tree Trader")
            
            try:
                trader_choice = input("Choose trader (1-3): ").strip()
                trader_types = {"1": "flowers", "2": "plants", "3": "trees"}
                
                if trader_choice in trader_types:
                    plant_type = trader_types[trader_choice]
                    shop.display_shop(shop_type=plant_type)
                    
                    seed_name = input("Enter seed name to buy (or 'back'): ").strip()
                    if seed_name.lower() != 'back' and seed_name in shop.seeds_for_sale:
                        if shop.buy_seed(seed_name, farm):
                            print(f"Bought {seed_name}!")
                        else:
                            print("Cannot buy seed! Check money, stock, or requirements.")
                    elif seed_name.lower() != 'back':
                        print("Seed not found!")
                else:
                    print("Invalid trader choice!")
            except (EOFError, KeyboardInterrupt):
                print("Cancelled!")

        elif choice == "6":
            print("What would you like to buy?")
            print("1. Tools")
            print("2. Fertilizers")
            
            try:
                buy_choice = input("Choose category (1-2): ").strip()
                
                if buy_choice == "1":
                    shop.display_shop(shop_type="tools")
                    tool_name = input("Enter tool name to buy (or 'back'): ").strip()
                    if tool_name.lower() != 'back' and tool_name in shop.tools_for_sale:
                        if shop.buy_tool(tool_name, farm):
                            print(f"Bought {tool_name}!")
                        else:
                            print("Cannot buy tool! Check money or if already owned.")
                    elif tool_name.lower() != 'back':
                        print("Tool not found!")
                        
                elif buy_choice == "2":
                    shop.display_shop(shop_type="fertilizer")
                    fert_name = input("Enter fertilizer name to buy (or 'back'): ").strip()
                    if fert_name.lower() != 'back' and fert_name in shop.fertilizers_for_sale:
                        if shop.buy_fertilizer(fert_name, farm):
                            print(f"Bought {fert_name}!")
                        else:
                            print("Cannot buy fertilizer! Check money.")
                    elif fert_name.lower() != 'back':
                        print("Fertilizer not found!")
                else:
                    print("Invalid choice!")
            except (EOFError, KeyboardInterrupt):
                print("Cancelled!")

        elif choice == "7":
            if not farm.inventory:
                print("No crops to sell!")
                continue
            
            print("Your harvested crops:")
            crops_list = list(farm.inventory.items())
            for i, (crop_name, count) in enumerate(crops_list):
                price = shop.crop_prices.get(crop_name, 1)
                print(f"{i + 1}. {crop_name} (x{count}) - ${price} each")
            
            try:
                crop_choice = int(input("Which crop to sell? ")) - 1
                if 0 <= crop_choice < len(crops_list):
                    crop_name, available = crops_list[crop_choice]
                    amount = int(input(f"How many {crop_name} to sell? (max {available}): "))
                    if 1 <= amount <= available:
                        total_earned = shop.sell_crop_to_shop(crop_name, amount, farm)
                        if total_earned > 0:
                            print(f"Sold {amount} {crop_name} for ${total_earned}!")
                        else:
                            print("Sale failed!")
                    else:
                        print("Invalid amount!")
                else:
                    print("Invalid choice!")
            except (ValueError, EOFError, KeyboardInterrupt):
                print("Invalid input!")

        elif choice == "8":
            try:
                print("Filter options:")
                print("Rarity: common, rare, epic, legendary")
                print("Traders: flowers, plants, trees, tools, fertilizer")
                
                filter_type = input("Enter filter type: ").lower().strip()
                if filter_type in ["common", "rare", "epic", "legendary"]:
                    shop.display_shop(filter_rarity=filter_type)
                elif filter_type in ["flowers", "plants", "trees", "tools", "fertilizer"]:
                    shop.display_shop(shop_type=filter_type)
                else:
                    print("Invalid filter!")
            except (EOFError, KeyboardInterrupt):
                print("Cancelled!")

        elif choice == "9":
            if not farm.crops:
                print("No crops to water!")
                continue
            
            watering_crops = [i for i, crop in enumerate(farm.crops) if crop.needs_watering]
            if not watering_crops:
                print("No crops need watering!")
                continue
            
            print("Crops that need watering:")
            for i in watering_crops:
                crop = farm.crops[i]
                time_since_water = farm.day - crop.last_watered
                print(f"{i + 1}. {crop.name} (last watered {time_since_water:.1f} days ago)")
            
            try:
                crop_choice = int(input("Which crop to water? ")) - 1
                if crop_choice in watering_crops:
                    if farm.water_crop(crop_choice):
                        print(f"Watered {farm.crops[crop_choice].name}!")
                    else:
                        print("Watering failed!")
                else:
                    print("Invalid choice!")
            except (ValueError, EOFError, KeyboardInterrupt):
                print("Invalid input!")

        elif choice == "10":
            print("Available sheds:")
            print("1. Flat Home - $500 (4 flower plots)")
            print("2. Modern Barn - $1,500 (8 flower + 8 plant plots)")
            print("3. Science Lab - $5,000 (includes lab access)")
            print("4. Biosphere - $15,000 (full facility with trees)")
            
            try:
                shed_choice = input("Choose shed (1-4): ").strip()
                shed_types = {"1": "Flat Home", "2": "Modern Barn", "3": "Science Lab", "4": "Biosphere"}
                
                if shed_choice in shed_types:
                    shed_name = shed_types[shed_choice]
                    if farm.buy_shed(shed_name):
                        print(f"Bought {shed_name}!")
                    else:
                        print("Cannot buy shed! Check money.")
                else:
                    print("Invalid choice!")
            except (EOFError, KeyboardInterrupt):
                print("Cancelled!")

        elif choice == "11":
            if not farm.lab.owned:
                print(f"You need a lab! Buy Science Lab (${5000}) or Biosphere (${15000}).")
                continue
            
            print("Lab Operations:")
            print("1. Crossbreed Plants")
            print("2. Refine Materials")
            print("3. View Recipes")
            
            try:
                lab_choice = input("Choose operation (1-3): ").strip()
                
                if lab_choice == "1":
                    ready_crops = [i for i, crop in enumerate(farm.crops) if crop.is_ready]
                    if len(ready_crops) < 2:
                        print("Need at least 2 ready crops to crossbreed!")
                        continue
                    
                    print("Ready crops:")
                    for i in ready_crops:
                        crop = farm.crops[i]
                        print(f"{i + 1}. {crop.name}")
                    
                    crop1 = int(input("First crop: ")) - 1
                    crop2 = int(input("Second crop: ")) - 1
                    
                    result = farm.crossbreed_plants(crop1, crop2)
                    if result:
                        hybrid_name, hybrid_price = result
                        print(f"Created {hybrid_name} worth ${hybrid_price}!")
                        farm.inventory[hybrid_name] = farm.inventory.get(hybrid_name, 0) + 1
                        farm.crops.pop(max(crop1, crop2))
                        farm.crops.pop(min(crop1, crop2))
                    else:
                        print("Crossbreeding failed!")
                
                elif lab_choice == "2":
                    if not farm.inventory:
                        print("No materials to refine!")
                        continue
                    
                    print("Available materials:")
                    for crop_name in farm.inventory:
                        if crop_name in farm.lab.recipes:
                            refined = farm.lab.recipes[crop_name]
                            print(f"  {crop_name} → {refined}")
                    
                    material = input("Enter material to refine: ").strip()
                    if farm.refine_material(material):
                        refined = farm.lab.recipes[material]
                        print(f"Refined {material} into {refined}!")
                    else:
                        print("Refining failed!")
                
                elif lab_choice == "3":
                    print("Lab Recipes:")
                    for material, product in farm.lab.recipes.items():
                        print(f"  {material} → {product}")
                        
            except (ValueError, EOFError, KeyboardInterrupt):
                print("Invalid input!")

        elif choice == "12":
            if not farm.shed or farm.shed.name != "Biosphere":
                print("Polytechnics require the Biosphere facility!")
                continue
            
            print("Polytechnic Upgrades:")
            for name, poly in farm.polytechnics.items():
                max_level = poly.max_level
                current = poly.current_level
                if current < max_level:
                    cost = poly.cost_per_level[current]
                    can_upgrade = farm.can_upgrade_polytechnic(name)
                    status = "Available" if can_upgrade else "Locked (balance other levels)"
                    print(f"  {name}: Level {current}/{max_level} - ${cost} ({status})")
                else:
                    print(f"  {name}: Level {current}/{max_level} - MAX LEVEL")
                print(f"    {poly.description}")
            
            try:
                poly_name = input("Enter polytechnic name to upgrade: ").strip()
                if poly_name in farm.polytechnics:
                    if farm.upgrade_polytechnic(poly_name):
                        new_level = farm.polytechnics[poly_name].current_level
                        print(f"Upgraded {poly_name} to level {new_level}!")
                    else:
                        print("Cannot upgrade! Check requirements and money.")
                else:
                    print("Polytechnic not found!")
            except (EOFError, KeyboardInterrupt):
                print("Cancelled!")

        elif choice == "13":
            print("Thank you for playing! Your farming empire awaits your return!")
            game_running = False
        
        else:
            print("Invalid choice! Please enter a number 1-13.")

if __name__ == "__main__":
    main()
