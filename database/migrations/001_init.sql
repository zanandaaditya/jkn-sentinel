CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


CREATE TABLE users (

id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

username VARCHAR(100) UNIQUE NOT NULL,

email VARCHAR(150),

created_at TIMESTAMP DEFAULT NOW()

);



CREATE TABLE claims (

id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

claim_code VARCHAR(50) UNIQUE NOT NULL,

provider_id VARCHAR(50),

claim_amount NUMERIC,

status VARCHAR(50),

created_at TIMESTAMP DEFAULT NOW()

);
