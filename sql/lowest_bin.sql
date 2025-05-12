SELECT item_name, MIN(start_bid), COUNT(*)
FROM Skyblock.Auction
GROUP BY item_name;