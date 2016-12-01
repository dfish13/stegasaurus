CREATE DATABASE steganography;
DO
$$
BEGIN
	IF NOT EXISTS (
		SELECT *
		FROM   pg_catalog.pg_user
		WHERE  usename = 'team') THEN
		CREATE USER team WITH PASSWORD 'password';
	END IF;

	ALTER ROLE team SET client_encoding TO 'utf8';
	ALTER ROLE team SET default_transaction_isolation TO 'read committed';
	ALTER ROLE team SET timezone TO 'UTC';
	ALTER USER team CREATEDB;
	GRANT ALL PRIVILEGES ON DATABASE steganography TO team;
END
$$
