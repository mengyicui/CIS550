8. List all choices of Toyota produced after 2010 with mileage between 50000-100000.

SELECT c.model, c.year, u.price, u.kilometer
FROM used_cars_info u, cars c
WHERE u.vehicle_model = c.model 
	AND u.vehicle_brand = c.make
	AND u.vehicle_brand = 'Toyota'
GROUP BY c.model, c.year, u.price, u.kilometer
HAVING u.kilometer > 50000
	AND u.kilometer < 100000
	AND c.year > 2010;

7.For Audi A5 model, what is the number of cars(per year) which were not produced in the same year as those price below 20000? Also show the choice of driven_wheels and doors_number. 

SELECT driven_wheels, doors_number, year, count(make) as count
FROM cars
WHERE year not in 
	(SELECT c.year
	FROM used_cars_info u JOIN cars c
	ON u.vehicle_brand = c.make AND u.vehicle_model = c.model
	WHERE vehicle_model = 'a5' AND vehicle_brand = 'Audi' And price < 20000)
GROUP BY year;

9. Print average price every model of front_wheel_driven used Volkswagen with fuel_consumption less than average. Order by the price. 

SELECT avg(price), vehicle_model
FROM used_cars_info u INNER JOIN (SELECT c.model
			FROM cars_addition ca INNER JOIN cars c
				ON ca.model = c.model AND ca.make = c.make
			WHERE c.driven_wheels = 'F' 
				AND c.make = 'Volkswagen'
				AND ca.average_consumption <
					(SELECT avg(average_consumption)
					FROM cars_addition
					WHERE make = 'Volkswagen')) A
ON u.vehicle_model = A.model
GROUP BY u.vehicle_model
ORDER BY u.price;
		
