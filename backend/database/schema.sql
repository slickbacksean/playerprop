-- Sports Prop Predictor Database Schema
-- Comprehensive schema defining table structures and constraints

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'regular', 'premium')),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);

-- Create indexes for performance
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- Predictions Table
CREATE TABLE predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id),
    sport VARCHAR(50) NOT NULL,
    event VARCHAR(100) NOT NULL,
    prop_type VARCHAR(50) NOT NULL,
    predicted_value FLOAT NOT NULL,
    actual_value FLOAT,
    odds FLOAT,
    potential_winnings FLOAT,
    prediction_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    event_date TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (
        status IN ('pending', 'correct', 'incorrect', 'cancelled')
    )
);

-- Indexes for predictions
CREATE INDEX idx_predictions_user ON predictions(user_id);
CREATE INDEX idx_predictions_sport ON predictions(sport);
CREATE INDEX idx_predictions_event ON predictions(event);
CREATE INDEX idx_predictions_status ON predictions(status);

-- Odds Table
CREATE TABLE odds (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sport VARCHAR(50) NOT NULL,
    event VARCHAR(100) NOT NULL,
    prop_type VARCHAR(50) NOT NULL,
    odds_type VARCHAR(20) NOT NULL CHECK (
        odds_type IN ('moneyline', 'spread', 'prop', 'total')
    ),
    value FLOAT NOT NULL,
    implied_probability FLOAT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    event_date TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Indexes for odds
CREATE INDEX idx_odds_sport ON odds(sport);
CREATE INDEX idx_odds_event ON odds(event);
CREATE INDEX idx_odds_timestamp ON odds(timestamp);