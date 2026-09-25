CREATE TABLE participants (

id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

participant_number VARCHAR(20) UNIQUE NOT NULL,

name VARCHAR(100),

gender VARCHAR(20),

birth_date DATE,

membership_type VARCHAR(20),

status VARCHAR(20),

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE providers (

id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

provider_code VARCHAR(50) UNIQUE,

provider_name VARCHAR(150),

provider_type VARCHAR(50),

province VARCHAR(100),

class VARCHAR(20),

status VARCHAR(20),

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE doctors (

id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

doctor_code VARCHAR(50),

name VARCHAR(100),

speciality VARCHAR(100),

provider_id UUID REFERENCES providers(id),

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE diagnosis (

id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

icd_code VARCHAR(20),

name VARCHAR(150),

category VARCHAR(100)

);

CREATE TABLE procedures (

id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

procedure_code VARCHAR(50),

name VARCHAR(150),

category VARCHAR(100),

standard_cost NUMERIC(14,2)

);

CREATE TABLE medicines (

id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

medicine_code VARCHAR(50),

name VARCHAR(150),

category VARCHAR(100),

standard_price NUMERIC(14,2)

);

