CREATE TABLE states (
    id INTEGER NOT NULL,
    name VARCHAR(20) NOT NULL,
    uf VARCHAR(2) NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE civil_states (
    id INTEGER NOT NULL,
    description VARCHAR(15) NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE zones (
    id INTEGER NOT NULL,
    description VARCHAR(40) NOT NULL,
    complement VARCHAR(10),
    PRIMARY KEY (id)
);
CREATE TABLE doctors (
    id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    crm VARCHAR(20) NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE ethnicities (
    id INTEGER NOT NULL,
    description VARCHAR(10) NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE user_types (
    id INTEGER NOT NULL,
    description VARCHAR(25) NOT NULL,
    role VARCHAR(10) NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE cities (
    id INTEGER NOT NULL,
    name VARCHAR(40) NOT NULL,
    state_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(state_id) REFERENCES states (id)
);
CREATE TABLE graves (
    id INTEGER NOT NULL,
    street VARCHAR(5) NOT NULL,
    number VARCHAR(5) NOT NULL,
    zone_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(zone_id) REFERENCES zones (id)
);
CREATE TABLE users (
    id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    login VARCHAR(30) NOT NULL,
    _pwd_hash VARCHAR(255) NOT NULL,
    user_type_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(user_type_id) REFERENCES user_types (id)
);
CREATE TABLE addresses (
    id INTEGER NOT NULL,
    street VARCHAR(255) NOT NULL,
    district VARCHAR(255) NOT NULL,
    cep VARCHAR(8) NOT NULL,
    city_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(city_id) REFERENCES cities (id)
);
CREATE TABLE registries (
    id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    city_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(city_id) REFERENCES cities (id)
);
CREATE TABLE deceased (
    id INTEGER NOT NULL,
    name VARCHAR(255),
    age INTEGER,
    birth_date DATE,
    death_datetime DATETIME NOT NULL,
    gender VARCHAR(1) NOT NULL,
    home_address_number VARCHAR(5),
    home_address_complement VARCHAR(255),
    filiations VARCHAR(512),
    registration VARCHAR(40) NOT NULL,
    cause VARCHAR(1500) NOT NULL,
    annotation VARCHAR(1500),
    death_address_number VARCHAR(5),
    death_address_complement VARCHAR(255),
    birthplace_id INTEGER,
    civil_state_id INTEGER,
    ethnicity_id INTEGER NOT NULL,
    home_address_id INTEGER,
    death_address_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    grave_id INTEGER NOT NULL,
    registry_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(birthplace_id) REFERENCES cities (id),
    FOREIGN KEY(civil_state_id) REFERENCES civil_states (id),
    FOREIGN KEY(ethnicity_id) REFERENCES ethnicities (id),
    FOREIGN KEY(home_address_id) REFERENCES addresses (id),
    FOREIGN KEY(death_address_id) REFERENCES addresses (id),
    FOREIGN KEY(doctor_id) REFERENCES doctors (id),
    FOREIGN KEY(grave_id) REFERENCES graves (id),
    FOREIGN KEY(registry_id) REFERENCES registries (id)
);
