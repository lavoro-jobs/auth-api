CREATE EXTENSION "uuid-ossp";

CREATE TYPE user_role AS ENUM ('applicant', 'recruiter');

CREATE TABLE IF NOT EXISTS accounts (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role user_role NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    created_on TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS verification_tokens (
    token VARCHAR(255) NOT NULL PRIMARY KEY UNIQUE,
    account_id uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    expiry_date TIMESTAMP NOT NULL DEFAULT NOW() + INTERVAL '48 hours'
);


CREATE OR REPLACE FUNCTION delete_confirmed_token() RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM verification_tokens WHERE account_id = OLD.id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delete_confirmed_token
AFTER UPDATE ON accounts 
FOR EACH ROW WHEN (OLD.is_active = FALSE AND NEW.is_active = TRUE)
EXECUTE FUNCTION delete_confirmed_token();

CREATE OR REPLACE FUNCTION delete_expired_tokens() RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM verification_tokens WHERE expiry_date < NOW();
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delete_expired_tokens
AFTER INSERT ON verification_tokens
FOR EACH ROW
EXECUTE FUNCTION delete_expired_tokens();
