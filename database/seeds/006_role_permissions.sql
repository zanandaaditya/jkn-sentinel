-- SYSTEM ADMIN SEMUA AKSES

INSERT INTO role_permissions
(role_id, permission_id)

SELECT
r.id,
p.id

FROM roles r, permissions p

WHERE r.name='SYSTEM_ADMIN';



-- FRAUD ANALYST

INSERT INTO role_permissions
(role_id, permission_id)

SELECT
r.id,
p.id

FROM roles r, permissions p

WHERE r.name='FRAUD_ANALYST'
AND p.code IN
(
'VIEW_DASHBOARD',
'VIEW_CLAIM',
'VIEW_RISK',
'INVESTIGATE_CASE'
);



-- MEDICAL REVIEWER

INSERT INTO role_permissions
(role_id, permission_id)

SELECT
r.id,
p.id

FROM roles r, permissions p

WHERE r.name='MEDICAL_REVIEWER'
AND p.code IN
(
'VIEW_DASHBOARD',
'VIEW_CLAIM'
);



-- PROVIDER REVIEWER

INSERT INTO role_permissions
(role_id, permission_id)

SELECT
r.id,
p.id

FROM roles r, permissions p

WHERE r.name='PROVIDER_REVIEWER'
AND p.code IN
(
'VIEW_DASHBOARD',
'VIEW_CLAIM'
);



-- AUDITOR

INSERT INTO role_permissions
(role_id, permission_id)

SELECT
r.id,
p.id

FROM roles r, permissions p

WHERE r.name='AUDITOR'
AND p.code IN
(
'VIEW_DASHBOARD',
'VIEW_AUDIT'
);



-- VIEWER

INSERT INTO role_permissions
(role_id, permission_id)

SELECT
r.id,
p.id

FROM roles r, permissions p

WHERE r.name='VIEWER'
AND p.code='VIEW_DASHBOARD';