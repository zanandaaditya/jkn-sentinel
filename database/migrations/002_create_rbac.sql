CREATE TABLE roles (

id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

name VARCHAR(50) UNIQUE NOT NULL,

description TEXT

);



CREATE TABLE permissions (

id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

code VARCHAR(100) UNIQUE NOT NULL,

description TEXT

);



CREATE TABLE user_roles (

user_id UUID REFERENCES users(id),

role_id UUID REFERENCES roles(id),

PRIMARY KEY(user_id, role_id)

);



CREATE TABLE role_permissions (

role_id UUID REFERENCES roles(id),

permission_id UUID REFERENCES permissions(id),

PRIMARY KEY(role_id, permission_id)

);
