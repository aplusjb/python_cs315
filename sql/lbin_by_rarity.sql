WITH lbin AS (SELECT item_name, MIN(start_bid) AS lowest
                    FROM Skyblock.Auction
                    WHERE bin = 1
                    GROUP BY item_name)
SELECT a.rarity, AVG(lbin.lowest)
FROM lbin NATURAL JOIN Skyblock.Auction AS a
GROUP BY a.rarity
ORDER BY AVG(lbin.lowest) DESC;