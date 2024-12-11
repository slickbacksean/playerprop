-- Query Optimization Strategies
-- Includes materialized views, indexes, and performance tuning

-- Materialized View: User Prediction Performance
CREATE MATERIALIZED VIEW user_prediction_stats AS
SELECT 
    user_id,
    COUNT(*) as total_predictions,
    SUM(CASE WHEN status = 'correct' THEN 1 ELSE 0 END) as correct_predictions,
    ROUND(
        100.0 * SUM(CASE WHEN status = 'correct' THEN 1 ELSE 0 END) / COUNT(*), 
        2
    ) as accuracy_percentage,
    AVG(potential_winnings) as avg_potential_winnings
FROM predictions
GROUP BY user_id
WITH DATA;

-- Create covering index for prediction search performance
CREATE INDEX idx_predictions_comprehensive ON predictions (
    user_id, 
    sport, 
    event_date, 
    status
) INCLUDE (predicted_value, actual_value, odds);

-- Optimize odds lookups
CREATE INDEX idx_odds_performance ON odds (
    sport, 
    event, 
    odds_type, 
    event_date
) INCLUDE (value, implied_probability);

-- Periodic refresh for materialized view
CREATE OR REPLACE FUNCTION refresh_user_prediction_stats()
RETURNS TRIGGER AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY user_prediction_stats;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_prediction_stats
AFTER INSERT OR UPDATE OR DELETE ON predictions
FOR EACH STATEMENT EXECUTE FUNCTION refresh_user_prediction_stats();

-- Example complex query with performance considerations
CREATE OR REPLACE FUNCTION get_user_prop_performance(
    p_user_id UUID, 
    p_sport VARCHAR(50)
) RETURNS TABLE (
    prop_type VARCHAR(50),
    total_predictions BIGINT,
    accuracy NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    WITH prop_stats AS (
        SELECT 
            prop_type,
            COUNT(*) as total_predictions,
            ROUND(
                100.0 * SUM(CASE WHEN status = 'correct' THEN 1 ELSE 0 END) / COUNT(*), 
                2
            ) as accuracy
        FROM predictions
        WHERE user_id = p_user_id AND sport = p_sport
        GROUP BY prop_type
    )
    SELECT * FROM prop_stats
    ORDER BY total_predictions DESC;
END;
$$ LANGUAGE plpgsql;