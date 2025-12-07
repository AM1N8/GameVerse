import pandas as pd

# Define the games based on the image URLs provided
games_data = [
    {
        "id": 1,
        "title": "Eternal Warfare",
        "description": "A gritty futuristic shooter where endless factions battle for supremacy on war-torn planets. Master tactical combat and lead your squad to victory.",
        "price": 49.99,
        "category": "FPS",
        "platform": "PC/Console",
        "release_year": 2024,
        "rating": "M",
        "multiplayer": "Yes",
        "developer": "Infinity Wardens",
        "image_url": "https://raw.githubusercontent.com/AM1N8/Dumpster/refs/heads/main/images/EternalWarfare.png"
    },
    {
        "id": 2,
        "title": "Cyber Nexus 2077",
        "description": "Dive into a neon-soaked metropolis in this open-world RPG. Hack, sneak, and fight your way through a corporate-controlled dystopia.",
        "price": 59.99,
        "category": "Action RPG",
        "platform": "PC/PS5/Xbox",
        "release_year": 2023,
        "rating": "M",
        "multiplayer": "No",
        "developer": "Neon Logic",
        "image_url": "https://raw.githubusercontent.com/AM1N8/Dumpster/refs/heads/main/images/cyberNexus2077.png"
    },
    {
        "id": 3,
        "title": "Kingdom Builders",
        "description": "Construct and manage your own medieval kingdom. Balance economy, defense, and happiness in this charming city-building simulation.",
        "price": 29.99,
        "category": "Strategy",
        "platform": "PC",
        "release_year": 2022,
        "rating": "E",
        "multiplayer": "Yes",
        "developer": "Crown Studios",
        "image_url": "https://raw.githubusercontent.com/AM1N8/Dumpster/refs/heads/main/images/KingdomBuilders.png"
    },
    {
        "id": 4,
        "title": "Pixel Dungeon Quest",
        "description": "Explore procedurally generated dungeons in this retro-style roguelike. Collect loot, defeat bosses, and uncover ancient secrets.",
        "price": 14.99,
        "category": "Roguelike",
        "platform": "PC/Switch",
        "release_year": 2021,
        "rating": "T",
        "multiplayer": "Yes",
        "developer": "BitMap Games",
        "image_url": "https://raw.githubusercontent.com/AM1N8/Dumpster/refs/heads/main/images/PixelDungeonQuest.png"
    },
    {
        "id": 5,
        "title": "Mystic Legends",
        "description": "Embark on an epic journey through a magical world. Master elemental spells and recruit companions in this classic turn-based RPG.",
        "price": 39.99,
        "category": "RPG",
        "platform": "PC/Console",
        "release_year": 2023,
        "rating": "T",
        "multiplayer": "No",
        "developer": "Fable Forge",
        "image_url": "https://raw.githubusercontent.com/AM1N8/Dumpster/refs/heads/main/images/MysticLegends.png"
    },
    {
        "id": 6,
        "title": "Shadow Assassin",
        "description": "Become a master of stealth in feudal Japan. Utilize shadows, tools, and agility to eliminate targets without being seen.",
        "price": 44.99,
        "category": "Stealth Action",
        "platform": "PC/Console",
        "release_year": 2024,
        "rating": "M",
        "multiplayer": "No",
        "developer": "Silent Blade",
        "image_url": "https://raw.githubusercontent.com/AM1N8/Dumpster/refs/heads/main/images/ShadowAssassin.png"
    },
    {
        "id": 7,
        "title": "Starbound Odyssey",
        "description": "Chart a course through the unknown reaches of the galaxy. Trade, fight, and discover new alien species in this space exploration sim.",
        "price": 34.99,
        "category": "Simulation",
        "platform": "PC",
        "release_year": 2022,
        "rating": "E10+",
        "multiplayer": "No",
        "developer": "Galactic Soft",
        "image_url": "https://raw.githubusercontent.com/AM1N8/Dumpster/refs/heads/main/images/StarboundOdyssy.png"
    },
    {
        "id": 8,
        "title": "Velocity Racer X",
        "description": "High-octane arcade racing at breakneck speeds. Customize your vehicle and dominate the tracks in a futuristic racing league.",
        "price": 24.99,
        "category": "Racing",
        "platform": "PC/Console",
        "release_year": 2023,
        "rating": "E",
        "multiplayer": "Yes",
        "developer": "Redline Games",
        "image_url": "https://raw.githubusercontent.com/AM1N8/Dumpster/refs/heads/main/images/VelocityRacerX.png"
    }
]

# Create DataFrame
df = pd.DataFrame(games_data)

# Save to CSV
df.to_csv("games.csv", index=False)