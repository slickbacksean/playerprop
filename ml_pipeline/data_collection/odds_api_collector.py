import os
import json
import requests
import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta
from requests.exceptions import RequestException

class OddsAPICollector:
    def __init__(self, api_key: str, base_url: str = 'https://api.the-odds-api.com/v4/sports'):
        """
        Initialize Odds API data collector.
        
        Args:
            api_key (str): API key for authentication
            base_url (str): Base URL for the Odds API
        """
        self.api_key = api_key
        self.base_url = base_url
        self.logger = logging.getLogger('OddsAPICollector')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Ensure data storage directory exists
        self.data_dir = os.path.join('data', 'odds')
        os.makedirs(self.data_dir, exist_ok=True)

    def fetch_sports_odds(self, 
                           sport: str, 
                           regions: str = 'us', 
                           markets: str = 'h2h,spreads', 
                           days_ahead: int = 7) -> List[Dict[Any, Any]]:
        """
        Fetch sports odds from the API.
        
        Args:
            sport (str): Sport to fetch odds for
            regions (str): Betting regions
            markets (str): Betting markets to include
            days_ahead (int): Number of days to fetch future events
        
        Returns:
            List of odds data
        """
        end_date = datetime.now() + timedelta(days=days_ahead)
        
        try:
            params = {
                'apiKey': self.api_key,
                'sport': sport,
                'regions': regions,
                'markets': markets,
                'oddsFormat': 'decimal'
            }
            
            response = requests.get(f'{self.base_url}/{sport}/odds', params=params)
            response.raise_for_status()
            
            odds_data = response.json()
            
            # Save raw data
            self._save_raw_data(sport, odds_data)
            
            return odds_data
        
        except RequestException as e:
            self.logger.error(f"Error fetching odds for {sport}: {e}")
            return []

    def _save_raw_data(self, sport: str, data: List[Dict[Any, Any]]):
        """
        Save raw odds data to a JSON file.
        
        Args:
            sport (str): Sport name
            data (List[Dict]): Odds data to save
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'{sport}_odds_{timestamp}.json'
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            self.logger.info(f"Saved odds data to {filepath}")
        except Exception as e:
            self.logger.error(f"Error saving odds data: {e}")

    def fetch_multiple_sports(self, sports_list: List[str]) -> Dict[str, List[Dict[Any, Any]]]:
        """
        Fetch odds for multiple sports.
        
        Args:
            sports_list (List[str]): List of sports to fetch
        
        Returns:
            Dict of sports and their corresponding odds
        """
        all_odds = {}
        for sport in sports_list:
            sport_odds = self.fetch_sports_odds(sport)
            if sport_odds:
                all_odds[sport] = sport_odds
        
        return all_odds

def main():
    """
    Example usage of OddsAPICollector
    """
    # Note: Replace with actual API key
    API_KEY = os.getenv('ODDS_API_KEY', '')
    
    if not API_KEY:
        print("Error: No API key found. Set ODDS_API_KEY environment variable.")
        return
    
    collector = OddsAPICollector(API_KEY)
    
    # Example: Fetch odds for multiple sports
    sports = ['basketball_nba', 'football_nfl', 'baseball_mlb']
    all_odds = collector.fetch_multiple_sports(sports)
    
    # Print summary
    for sport, odds in all_odds.items():
        print(f"{sport}: {len(odds)} events")

if __name__ == "__main__":
    main()