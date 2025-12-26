DROP TABLE IF EXISTS listings;

CREATE TABLE listings (
    listing_id INTEGER PRIMARY KEY,
    name TEXT,
    host_id INTEGER,
    neighborhood TEXT,
    room_type TEXT,
    price REAL,
    minimum_nights INTEGER,
    number_of_reviews INTEGER,
    reviews_per_month REAL,
    availability_365 INTEGER,
    instant_bookable INTEGER,
    price_tier TEXT,
    has_reviews INTEGER,
    ab_group TEXT,
    booking_rate REAL,
    bookings INTEGER,
    revenue REAL
);

-- Create index on ab_group for faster queries
CREATE INDEX idx_ab_group ON listings(ab_group);

-- Create index on neighborhood
CREATE INDEX idx_neighborhood ON listings(neighborhood);