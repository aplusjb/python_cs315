# CS-315 Project Part 2

### How to install requirements 
1) Make sure you have an environment folder and `cd` to it
2) `pip install -r requirements.txt`

## Task 1
The insert queries were created with [generate_insert.py](generate_insert.py), which was run separately from main.py. I was using the [Hypixel Public API](https://api.hypixel.net/) to request game data, which is then written into [insert.sql](sql/insert.sql). Unfortunately, the Bid table remains empty, as my API key was (understandably) throttled for spamming too many requests :(

## Task 2

## Task 3
![schema_image](screenshots/skyblock_schema.png)
***
a. This schema is intended to store game data from the Minecraft server Hypixel’s API. The model could be useful for storing player data in any MMO game, especially if more columns were added to the Profile and Player tables to keep complete records of player data. The model could even be adapted to real-life online auction platforms, relating accounts to auctions rather than players in a game. 
***
b. Players can create multiple save slots (or profiles), and may list or bid on auctions from any of those profiles. A profile can also have multiple players, and players on the same profile can see and collect each other’s auctions. Thus, the Profile table is related to Auction, and the Player table to Profile. Each unique auction can have multiple bids, so there is also the Bid table, pointing to the player/profile bidding, and the auction they are bidding on.

If there were more data stored about each profile, such as the date the first member created it, we would want to make a linking table between Profile and Player (as it is a many-to-many relationship), but in this case I am only storing the date each player joined the profile, so it is unnecessary.

I chose this model because I knew I could populate it with real data and learn to make API requests. The game is also an application I am familiar with and enjoy.