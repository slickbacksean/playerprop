"""
Alembic migration script for Sports Prop Predictor database initialization.

Handles comprehensive schema creation, versioning, and incremental changes.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Revision identifiers
revision = 'initial_setup'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    """
    Apply comprehensive database schema upgrades.
    Creates tables, custom types, and defines initial schema with constraints.
    """
    # Enable UUID extension
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    
    # Create custom ENUM types
    op.execute("""
        CREATE TYPE user_role AS ENUM ('admin', 'regular', 'premium');
        CREATE TYPE prediction_status AS ENUM ('pending', 'correct', 'incorrect', 'cancelled');
        CREATE TYPE odds_type AS ENUM ('moneyline', 'spread', 'prop', 'total');
    """)
    
    # Users Table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), 
                  server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('username', sa.String(50), unique=True, nullable=False),
        sa.Column('email', sa.String(120), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('role', sa.Enum('admin', 'regular', 'premium', name='user_role'), 
                  nullable=False, default='regular'),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('is_verified', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), 
                  server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True)
    )
    
    # Predictions Table
    op.create_table(
        'predictions',
        sa.Column('id', postgresql.UUID(as_uuid=True), 
                  server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), 
                  sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('sport', sa.String(50), nullable=False),
        sa.Column('event', sa.String(100), nullable=False),
        sa.Column('prop_type', sa.String(50), nullable=False),
        sa.Column('predicted_value', sa.Float, nullable=False),
        sa.Column('actual_value', sa.Float, nullable=True),
        sa.Column('odds', sa.Float, nullable=True),
        sa.Column('potential_winnings', sa.Float, nullable=True),
        sa.Column('prediction_date', sa.DateTime(timezone=True), 
                  server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('event_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', sa.Enum('pending', 'correct', 'incorrect', 'cancelled', 
                                     name='prediction_status'), 
                  nullable=False, default='pending')
    )
    
    # Odds Table
    op.create_table(
        'odds',
        sa.Column('id', postgresql.UUID(as_uuid=True), 
                  server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('sport', sa.String(50), nullable=False),
        sa.Column('event', sa.String(100), nullable=False),
        sa.Column('prop_type', sa.String(50), nullable=False),
        sa.Column('odds_type', sa.Enum('moneyline', 'spread', 'prop', 'total', 
                                        name='odds_type'), nullable=False),
        sa.Column('value', sa.Float, nullable=False),
        sa.Column('implied_probability', sa.Float, nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), 
                  server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('event_date', sa.DateTime(timezone=True), nullable=False)
    )
    
    # Create comprehensive indexes
    op.create_index('idx_users_username', 'users', ['username'])
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_role', 'users', ['role'])
    
    op.create_index('idx_predictions_user', 'predictions', ['user_id'])
    op.create_index('idx_predictions_sport', 'predictions', ['sport'])
    op.create_index('idx_predictions_event', 'predictions', ['event'])
    op.create_index('idx_predictions_status', 'predictions', ['status'])
    
    op.create_index('idx_odds_sport', 'odds', ['sport'])
    op.create_index('idx_odds_event', 'odds', ['event'])
    op.create_index('idx_odds_timestamp', 'odds', ['timestamp'])
    
    # Create performance-optimized covering indexes
    op.execute("""
        CREATE INDEX idx_predictions_comprehensive ON predictions 
        USING btree (user_id, sport, event_date, status) 
        INCLUDE (predicted_value, actual_value, odds);
        
        CREATE INDEX idx_odds_performance ON odds 
        USING btree (sport, event, odds_type, event_date) 
        INCLUDE (value, implied_probability);
    """)

def downgrade():
    """
    Safely revert database schema to previous state.
    Drops tables, indexes, and custom types.
    """
    # Drop performance indexes
    op.execute("""
        DROP INDEX IF EXISTS idx_predictions_comprehensive;
        DROP INDEX IF EXISTS idx_odds_performance;
    """)
    
    # Drop standard indexes
    op.drop_index('idx_odds_timestamp', table_name='odds')
    op.drop_index('idx_odds_event', table_name='odds')
    op.drop_index('idx_odds_sport', table_name='odds')
    
    op.drop_index('idx_predictions_status', table_name='predictions')
    op.drop_index('idx_predictions_event', table_name='predictions')
    op.drop_index('idx_predictions_sport', table_name='predictions')
    op.drop_index('idx_predictions_user', table_name='predictions')
    
    op.drop_index('idx_users_role', table_name='users')
    op.drop_index('idx_users_email', table_name='users')
    op.drop_index('idx_users_username', table_name='users')
    
    # Drop tables
    op.drop_table('odds')
    op.drop_table('predictions')
    op.drop_table('users')
    
    # Remove custom types
    op.execute("""
        DROP TYPE IF EXISTS user_role;
        DROP TYPE IF EXISTS prediction_status;
        DROP TYPE IF EXISTS odds_type;
    """)
    
    # Disable UUID extension
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp"')

def create_triggers():
    """
    Optional method to create database triggers for additional functionality.
    """
    # Trigger to validate user predictions
    op.execute("""
        CREATE OR REPLACE FUNCTION validate_prediction()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Example validation logic
            IF NEW.predicted_value < 0 THEN
                RAISE EXCEPTION 'Predicted value cannot be negative';
            END IF;
            
            IF NEW.event_date < CURRENT_TIMESTAMP THEN
                RAISE EXCEPTION 'Cannot make predictions for past events';
            END IF;
            
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER check_prediction_validity
        BEFORE INSERT OR UPDATE ON predictions
        FOR EACH ROW
        EXECUTE FUNCTION validate_prediction();
    """)
    
    # Trigger to update user last login
    op.execute("""
        CREATE OR REPLACE FUNCTION update_last_login()
        RETURNS TRIGGER AS $$
        BEGIN
            UPDATE users 
            SET last_login = CURRENT_TIMESTAMP 
            WHERE id = NEW.id;
            
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER user_login_trigger
        AFTER INSERT OR UPDATE ON users
        FOR EACH ROW
        EXECUTE FUNCTION update_last_login();
    """)