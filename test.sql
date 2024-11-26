SELECT customers.customerid, customers.customername, orders.orderid, 
orders.orderdate, orders.quantity, products.productname, 
products.price, orders.quantity * products.price AS totalprice 
FROM Customers JOIN Orders ON customers.CustomerID = orders.customerID 
join products 
ON orders.productid = PRODUCTS.ProductID 
where orders.orderdate BETWEEN '2024-01-01' and '2024-12-31' 
AND Customers.region IN ('north', 'south', 'east', 'west') or products.price > 500 
GROUP by Customers.customerID, Customers.customerName, orders.orderID, 
orders.orderdate, orders.quantity, products.productName, Products.price 
HAVING sum(orders.quantity) > 100
ORDER BY Customers.customerName , orders.OrderDate DESC;
