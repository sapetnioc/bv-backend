CREATE TABLE identity
(
    login TEXT PRIMARY KEY,
    password TEXT,
    email TEXT,
    first_name TEXT,
    last_name TEXT,
    institution TEXT,
    registration_time TIMESTAMP,
    email_verification_time TIMESTAMP,
    activation_time TIMESTAMP,
    deactivation_time TIMESTAMP
);


CREATE TABLE role
(
    name TEXT PRIMARY KEY,
    description TEXT
);

CREATE TABLE granting
(
    role TEXT NOT NULL REFERENCES role ON UPDATE CASCADE,
    given_to TEXT NOT NULL REFERENCES role ON UPDATE CASCADE,
    inherit BOOL NOT NULL DEFAULT TRUE,
    PRIMARY KEY (role, given_to)
);

CREATE TABLE session
(
    id TEXT PRIMARY KEY,
    login TEXT NOT NULL REFERENCES identity ON UPDATE CASCADE,
    roles TEXT[]
);


INSERT INTO role VALUES ('identity_admin', 'can read or modify any identity');
INSERT INTO role VALUES ('active', 'this role is given to all active users');

INSERT INTO identity (login, password) VALUES ('admin', 'b6540e4c524891f55fd61b7b9b6f745ff227e8a6946cc0ce5d184a46676399443225769481bdf15918fe9f4f7f436f611c620fb6ee447890975510012d2cb772fc660960b484f4315e881e1cd0bf3f33f8a441ca73683cd6d04eb2dde9c75603');
INSERT INTO role VALUES ('$admin', 'role of user admin');

INSERT INTO granting VALUES ('identity_admin', '$admin', TRUE);
INSERT INTO granting VALUES ('active', '$admin', FALSE);
