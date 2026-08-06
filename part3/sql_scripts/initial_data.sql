PRAGMA foreign_keys = ON;

INSERT INTO users (
    id,
    first_name,
    last_name,
    email,
    password,
    is_admin
)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$nfBzCPjBkqDlhHwnGFJa/.HEaWQhwzxscBoLnNipaUp09A2Gv8ETq',
    TRUE
);

INSERT INTO amenities (id, name)
VALUES
    (
        '54f63ed9-a4af-499d-8d98-5b754c149d13',
        'WiFi'
    ),
    (
        'dcf90ab8-f772-45dc-9664-15aae6f4ade8',
        'Swimming Pool'
    ),
    (
        '6ca25900-4519-4e9e-955c-3e700e0705f1',
        'Air Conditioning'
    );