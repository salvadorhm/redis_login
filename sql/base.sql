.headers ON
.mode list

CREATE TABLE users(
    user TEXT PRIMARY KEY,
    password TEXT
);

INSERT INTO users(user,password)
VALUES
('user1','1234'),
('user2','5678');

SELECT * FROM users;

