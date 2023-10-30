CREATE EXTENSION "uuid-ossp";

CREATE TYPE user_role AS ENUM ('applicant', 'recruiter');

CREATE TABLE IF NOT EXISTS account (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role user_role NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    created_on TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS verification_token (
    token VARCHAR(255) NOT NULL PRIMARY KEY UNIQUE,
    account_id uuid NOT NULL REFERENCES account(id) ON DELETE CASCADE,
    expiry_date TIMESTAMP NOT NULL
);
