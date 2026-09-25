INSERT INTO user_roles
(user_id, role_id)

SELECT
u.id,
r.id

FROM users u, roles r

WHERE
u.username='admin.demo'
AND r.name='SYSTEM_ADMIN';



INSERT INTO user_roles
(user_id, role_id)

SELECT
u.id,
r.id

FROM users u, roles r

WHERE
u.username='analyst.demo'
AND r.name='FRAUD_ANALYST';



INSERT INTO user_roles
(user_id, role_id)

SELECT
u.id,
r.id

FROM users u, roles r

WHERE
u.username='medical.demo'
AND r.name='MEDICAL_REVIEWER';



INSERT INTO user_roles
(user_id, role_id)

SELECT
u.id,
r.id

FROM users u, roles r

WHERE
u.username='provider.demo'
AND r.name='PROVIDER_REVIEWER';



INSERT INTO user_roles
(user_id, role_id)

SELECT
u.id,
r.id

FROM users u, roles r

WHERE
u.username='auditor.demo'
AND r.name='AUDITOR';



INSERT INTO user_roles
(user_id, role_id)

SELECT
u.id,
r.id

FROM users u, roles r

WHERE
u.username='viewer.demo'
AND r.name='VIEWER';