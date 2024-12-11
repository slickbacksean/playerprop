-- Seed Data for Sports Prop Predictor
-- Provides initial data for testing and development

-- Sample Users
INSERT INTO users (
    username, email, password_hash, role, is_active, is_verified
) VALUES 
    ('admin', 'admin@sportsprops.com', 
     '$2b$12$abcdefghijklmnopqrstuvwx', 'admin', true, true),
    ('test_user', 'test@sportsprops.com', 
     '$2b$12$abcdefghijklmnopqrstuvwx', 'regular', true, true),
    ('premium_user', 'premium@sportsprops.com', 
     '$2b$12$abcdefghijklmnopqrstuvwx', 'premium', true, true);

-- Sample Predictions
INSERT INTO predictions (
    user_id, 
    sport, 
    event, 
    prop_type, 
    predicted_value, 
    odds, 
    potential_winnings, 
    prediction_date, 
    event_date, 
    status
) VALUES 
    (
        (SELECT id FROM users WHERE username = 'test_user'),
        'basketball', 
        'NBA Finals Game 1', 
        'total_points', 
        215.5, 
        1.95, 
        50.00, 
        CURRENT_TIMESTAMP, 
        CURRENT_TIMESTAMP + INTERVAL '7 days', 
        'pending'
    ),
    (
        (SELECT id FROM users WHERE username = 'premium_user'),
        'football', 
        'Super Bowl LVIII', 
        'quarterback_passing_yards', 
        289.5, 
        2.10, 
        100.00, 
        CURRENT_TIMESTAMP, 
        CURRENT_TIMESTAMP + INTERVAL '14 days', 
        'pending'
    );

-- Sample Odds
INSERT INTO odds (
    sport, 
    event, 
    prop_type, 
    odds_type, 
    value, 
    implied_probability, 
    timestamp, 
    event_date
) VALUES 
    (
        'basketball', 
        'NBA Finals Game 1', 
        'total_points', 
        'total', 
        215.5, 
        0.52, 
        CURRENT_TIMESTAMP, 
        CURRENT_TIMESTAMP + INTERVAL '7 days'
    ),
    (
        'football', 
        'Super Bowl LVIII', 
        'quarterback_passing_yards', 
        'prop', 
        289.5, 
        0.48, 
        CURRENT_TIMESTAMP, 
        CURRENT_TIMESTAMP + INTERVAL '14 days'
    );