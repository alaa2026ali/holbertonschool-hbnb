PRAGMA foreign_keys = ON;

-- READ: Verify administrator and amenities
SELECT id, first_name, last_name, email, is_admin
FROM users
WHERE email = 'admin@hbnb.io';

SELECT *
FROM amenities;

-- CREATE: Add a temporary user
INSERT INTO users (
    id,
    first_name,
    last_name,
    email,
    password,
    is_admin
)
VALUES (
    '11111111-1111-4111-8111-111111111111',
    'Test',
    'User',
    'test.user@hbnb.io',
    'temporary-hashed-password',
    FALSE
);

-- READ: Verify temporary user
SELECT *
FROM users
WHERE id = '11111111-1111-4111-8111-111111111111';

-- UPDATE: Update temporary user's first name
UPDATE users
SET first_name = 'Updated'
WHERE id = '11111111-1111-4111-8111-111111111111';

SELECT *
FROM users
WHERE id = '11111111-1111-4111-8111-111111111111';

-- DELETE: Remove temporary user
DELETE FROM users
WHERE id = '11111111-1111-4111-8111-111111111111';

SELECT *
FROM users
WHERE id = '11111111-1111-4111-8111-111111111111';