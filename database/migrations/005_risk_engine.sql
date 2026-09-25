CREATE TABLE risk_rules (

id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

rule_code VARCHAR(50) UNIQUE NOT NULL,

rule_name VARCHAR(150),

category VARCHAR(100),

description TEXT,

severity VARCHAR(20),

is_active BOOLEAN DEFAULT TRUE,

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE risk_assessments (

id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),


claim_id UUID
REFERENCES claims(id),


rule_id UUID
REFERENCES risk_rules(id),


risk_score NUMERIC(5,2),


risk_level VARCHAR(20),


detector_type VARCHAR(50),


explanation TEXT,


created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE fraud_labels (

id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),


claim_id UUID
REFERENCES claims(id),


label VARCHAR(50),


confidence NUMERIC(5,2),


verified_by UUID
REFERENCES users(id),


verification_status VARCHAR(30),


created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE model_versions (

id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),


model_name VARCHAR(100),


version VARCHAR(50),


algorithm VARCHAR(100),


accuracy NUMERIC(5,2),


created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);


CREATE TABLE prediction_logs (

id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),


claim_id UUID
REFERENCES claims(id),


model_id UUID
REFERENCES model_versions(id),


input_snapshot JSONB,


prediction_result JSONB,


created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);


CREATE TABLE feature_store (

id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),


claim_id UUID
REFERENCES claims(id),


feature_name VARCHAR(100),


feature_value NUMERIC,


created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);


