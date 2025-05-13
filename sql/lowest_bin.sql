SELECT item_name, MIN(start_bid), COUNT(*)
FROM Skyblock.Auction
WHERE bin = 1
GROUP BY item_name;