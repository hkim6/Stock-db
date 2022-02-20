DROP SCHEMA sales_cube CASCADE;
CREATE SCHEMA sales_cube;
	CREATE TABLE sales_cube.states(
		id			SERIAL PRIMARY KEY,
		name		VARCHAR(20) NOT NULL UNIQUE
	);
	CREATE TABLE sales_cube.customers(
		id          SERIAL PRIMARY KEY,
		first_name	VARCHAR(20) NOT NULL,
		last_name	VARCHAR(20) NOT NULL,
		state_id	INTEGER REFERENCES sales_cube.states (id) NOT NULL
	);
