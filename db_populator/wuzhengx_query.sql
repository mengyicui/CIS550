# select out the car brand, and make convertible type of vehicle,
# with highest engine hp, and it is produced after 2014.

SELECT DISTINCT C_OUT.make, C_OUT.model, C_OUT.year
FROM cars C_OUT INNER JOIN engine E_OUT
ON C_OUT.engine_code = E_OUT.engine_code
WHERE E_OUT.engine_hp = (
	SELECT max(E.engine_hp)
	FROM cars C INNER JOIN engine E
	ON C.engine_code = E.engine_code
	WHERE C.style = "Convertible"
	) AND C_OUT.year > 2014

# API call is needed for producing the final output of this query.
# select out brand "Audi"'s car exist in used car market with the largest hp, and is
# with in 100 miles of your input location zipcode https://www.zipcodeapi.com/API#distance
SELECT DISTINCT C.make, UC.postal_code, UC.year_of_registration, UC.price, UC.vehicle_model
FROM cars C INNER JOIN used_cars_info UC
			ON C.make = UC.vehicle_brand
			INNER JOIN engine E_OUT
			ON C.engine_code = E_OUT.engine_code
WHERE E_OUT.engine_hp > (
	SELECT avg(E_IN.engine_hp)
	FROM cars C_IN INNER JOIN engine E_IN
	ON C_IN.engine_code = E_IN.engine_code
	WHERE C_IN.make = "Audi"
	) AND C.make = "Audi" AND UC.year_of_registration > 2014;

# select out the sedan model with highest popularity, and with lowest msrp
SELECT C.make, C.model, max(C.popularity)
FROM cars C
WHERE msrp > (
		SELECT AVG(C_IN.msrp)
		FROM cars C_IN
	) AND exists (
		SELECT *
		FROM used_cars_info UC
		WHERE C.make = UC.vehicle_brand AND UC.year_of_registration > 2008
	) AND C.style = "Sedan";