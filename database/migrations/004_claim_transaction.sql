CREATE TABLE claims (

id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

claim_number VARCHAR(50) UNIQUE NOT NULL,

participant_id UUID 
REFERENCES participants(id),

provider_id UUID
REFERENCES providers(id),

doctor_id UUID
REFERENCES doctors(id),

diagnosis_id UUID
REFERENCES diagnosis(id),

service_date DATE,

admission_date DATE,

discharge_date DATE,

claim_type VARCHAR(50),

claim_amount NUMERIC(14,2),

approved_amount NUMERIC(14,2),

claim_status VARCHAR(30),

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE claim_details (

id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

claim_id UUID
REFERENCES claims(id)
ON DELETE CASCADE,


procedure_id UUID
REFERENCES procedures(id),


medicine_id UUID
REFERENCES medicines(id),


quantity INTEGER,


charged_amount NUMERIC(14,2),


created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE payments (

id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

claim_id UUID
REFERENCES claims(id),

payment_date DATE,

payment_amount NUMERIC(14,2),

payment_status VARCHAR(30),

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

