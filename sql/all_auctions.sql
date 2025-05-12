SELECT p.username, a.item_name, a.category, a.rarity, a.bin, a.start_bid, FROM_UNIXTIME(start_time/1000)
FROM Skyblock.Auction AS a
INNER JOIN Skyblock.Player AS p ON p.uuid = a.player_id;