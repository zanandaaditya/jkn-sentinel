CREATE TABLE investigation_cases (

id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

case_number VARCHAR(50) UNIQUE NOT NULL,


risk_assessment_id UUID
REFERENCES risk_assessments(id),


assigned_to UUID
REFERENCES users(id),


priority VARCHAR(20),


status VARCHAR(30),


summary TEXT,


resolution TEXT,


created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE case_comments (

id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),


case_id UUID
REFERENCES investigation_cases(id)
ON DELETE CASCADE,


user_id UUID
REFERENCES users(id),


comment TEXT,


created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE evidence (

id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),


case_id UUID
REFERENCES investigation_cases(id)
ON DELETE CASCADE,


evidence_type VARCHAR(50),


file_name VARCHAR(255),


file_path TEXT,


description TEXT,


uploaded_by UUID
REFERENCES users(id),


created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE case_history (

id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),


case_id UUID
REFERENCES investigation_cases(id),


action VARCHAR(100),


old_status VARCHAR(30),


new_status VARCHAR(30),


performed_by UUID
REFERENCES users(id),


created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE audit_logs (

id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),


user_id UUID
REFERENCES users(id),


action VARCHAR(100),


module VARCHAR(100),


record_id UUID,


description TEXT,


ip_address VARCHAR(50),


created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);