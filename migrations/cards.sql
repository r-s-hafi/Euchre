--creates the table if the table does not exist

DROP TABLE IF EXISTS deck;

CREATE TABLE IF NOT EXISTS deck (
    "id" TEXT NOT NULL,
    "suit" TEXT NOT NULL,
    "symbol" TEXT NOT NULL,
    "value" INTEGER NOT NULL
);

INSERT INTO deck (id, suit, symbol, value) VALUES

    ('9', 'Spades', '♠', 9),
    ('10', 'Spades', '♠', 10),
    ('J', 'Spades', '♠', 11),
    ('Q', 'Spades', '♠', 12),
    ('K', 'Spades', '♠', 13),
    ('A', 'Spades', '♠', 14),
    
    ('9', 'Clubs', '♣', 9),
    ('10', 'Clubs', '♣', 10),
    ('J', 'Clubs', '♣', 11),
    ('Q', 'Clubs', '♣', 12),
    ('K', 'Clubs', '♣', 13),
    ('A', 'Clubs', '♣', 14),

    ('9', 'Hearts', '♥', 9),
    ('10', 'Hearts', '♥', 10),
    ('J', 'Hearts', '♥', 11),
    ('Q', 'Hearts', '♥', 12),
    ('K', 'Hearts', '♥', 13),
    ('A', 'Hearts', '♥', 14),
    
    ('9', 'Diamonds', '♦', 9),
    ('10', 'Diamonds', '♦', 10),
    ('J', 'Diamonds', '♦', 11),
    ('Q', 'Diamonds', '♦', 12),
    ('K', 'Diamonds', '♦', 13),
    ('A', 'Diamonds', '♦', 14);


DROP TABLE IF EXISTS user_hand;

CREATE TABLE IF NOT EXISTS user_hand (
    "id" TEXT NOT NULL,
    "suit" TEXT NOT NULL,
    "symbol" TEXT NOT NULL,
    "value" INTEGER NOT NULL
);

DROP TABLE IF EXISTS bot1_hand;

CREATE TABLE IF NOT EXISTS bot1_hand (
    "id" TEXT NOT NULL,
    "suit" TEXT NOT NULL,
    "symbol" TEXT NOT NULL,
    "value" INTEGER NOT NULL
);

DROP TABLE IF EXISTS bot2_hand;

CREATE TABLE IF NOT EXISTS bot2_hand (
    "id" TEXT NOT NULL,
    "suit" TEXT NOT NULL,
    "symbol" TEXT NOT NULL,
    "value" INTEGER NOT NULL
);

DROP TABLE IF EXISTS bot3_hand;

CREATE TABLE IF NOT EXISTS bot3_hand (
    "id" TEXT NOT NULL,
    "suit" TEXT NOT NULL,
    "symbol" TEXT NOT NULL,
    "value" INTEGER NOT NULL
);


