CREATE TABLE unas_positions (
    id SERIAL PRIMARY KEY,
    position VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    photo VARCHAR(255) NOT NULL,
    type VARCHAR(255) NOT NULL,
    position_seller VARCHAR(255) NOT NULL,
    seller_photo VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL,
    seller_name VARCHAR(255) NOT NULL
);
