import os
import json
import logging
import requests
from typing import List, Dict, Any
from datetime import datetime, timedelta
from requests.exceptions import RequestException

class SportradarCollector:
    def __init__(self, api_key: str, base_url: str = 'https://api.sportradar.com/v1'):
        """
        Initialize Sportradar data collector.
        
        Args:
            api_key (str): API key for authentication
            base_url (str): Base URL for Sportradar API
        """
        self.api_key = api_key
        self.base_url = base_url
        self.logger = logging.getLogger('SportradarCollector')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Ensure data storage directory exists
        self.data_dir = os.path.join('data', 'sportradar')
        os.makedirs(self.data_dir, exist_ok=True)

    def fetch_team_statistics(self, sport: str, team_id: str) -> Dict[str, Any]:
        """
        Fetch detailed team statistics.
        
        Args:
            sport (str): Sport type (e.g., 'nba', 'nfl')
            team_id (str): Unique team identifier
        
        Returns:
            Dict containing team statistics
        """
        try:
            endpoint = f'{self.base_url}/{sport}/teams/{team_id}/statistics'
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Accept': 'application/json'
            }
            
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            
            team_stats = response.json()
            
            # Save raw data
            self._save_raw_data(f'{sport}_team_{team_id}_stats', team_stats)
            
            return team_stats
        
        except RequestException as e:
            self.logger.error(f"Error fetching team stats for {team_id}: {e}")
            return {}

    def fetch_player_performance(self, sport: str, player_id: str, days_back: int = 30) -> Dict[str, Any]:
        """
        Fetch player performance data for a specified period.
        
        Args:
            sport (str): Sport type
            player_id (str): Unique player identifier
            days_back (int): Number of days to fetch historical data
        
        Returns:
            Dict containing player performance metrics
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        try:
            endpoint = f'{self.base_url}/{sport}/players/{player_id}/performance'
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Accept': 'application/json'
            }
            
            params = {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d')
            }
            
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            
            player_performance = response.json()
            
            # Save raw data
            self._save_raw_data(f'{sport}_player_{player_id}_performance', player_performance)
            
            return player_performance
        
        except RequestException as e:
            self.logger.error(f"Error fetching player performance for {player_id}: {e}")
            return {}

    def fetch_game_schedule(self, sport: str, date: datetime = None) -> List[Dict[str, Any]]:
        """
        Fetch game schedule for a specific sport and date.
        
        Args:
            sport (str): Sport type
            date (datetime, optional): Date to fetch schedule for. Defaults to today.
        
        Returns:
            List of game schedules
        """
        if date is None:
            date = datetime.now()
        
        try:
            endpoint = f'{self.base_url}/{sport}/schedule'
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Accept': 'application/json'
            }
            
            params = {
                'date': date.strftime('%Y-%m-%d')
            }
            
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            
            game_schedule = response.json()
            
            # Save raw data
            self._save_raw_data(f'{sport}_schedule_{date.strftime("%Y%m%d")}', game_schedule)
            
            return game_schedule
        
        except RequestException as e:
            self.logger.error(f"Error fetching game schedule for {sport} on {date}: {e}")
            return []

    def _save_raw_data(self, filename: str, data: Dict[str, Any] | List[Dict[str, Any]]):
        """
        Save raw data to a JSON file.
        
        Args:
            filename (str): Base filename for the saved data
            data (Dict or List): Data to save
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        full_filename = f'{filename}_{timestamp}.json'
        filepath = os.path.join(self.data_dir, full_filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            self.logger.info(f"Saved data to {filepath}")
        except Exception as e:
            self.logger.error(f"Error saving data: {e}")

    def bulk_data_collection(self, 
                              sport: str, 
                              team_ids: List[str], 
                              player_ids: List[str], 
                              days_back: int = 30) -> Dict[str, Any]:
        """
        Perform bulk data collection for multiple teams and players.
        
        Args:
            sport (str): Sport type
            team_ids (List[str]): List of team identifiers
            player_ids (List[str]): List of player identifiers
            days_back (int): Number of days to fetch historical data
        
        Returns:
            Comprehensive data collection dictionary
        """
        collected_data = {
            'sport': sport,
            'teams': {},
            'players': {},
            'schedule': self.fetch_game_schedule(sport)
        }
        
        # Collect team statistics
        for team_id in team_ids:
            collected_data['teams'][team_id] = self.fetch_team_statistics(sport, team_id)
        
        # Collect player performances
        for player_id in player_ids:
            collected_data['players'][player_id] = self.fetch_player_performance(sport, player_id, days_back)
        
        return collected_data

def main():
    """
    Example usage of SportradarCollector
    """
    # Note: Replace with actual API key
    API_KEY = os.getenv('SPORTRADAR_API_KEY', '')
    
    if not API_KEY:
        print("Error: No API key found. Set SPORTRADAR_API_KEY environment variable.")
        return
    
    collector = SportradarCollector(API_KEY)
    
    # Example: Bulk data collection for NBA
    bulk_data = collector.bulk_data_collection(
        sport='nba', 
        team_ids=['team1', 'team2'],  # Replace with actual team IDs
        player_ids=['player1', 'player2']  # Replace with actual player IDs
    )
    
    # Print summary
    print(f"Collected data for NBA:")
    print(f"Teams: {len(bulk_data['teams'])}")
    print(f"Players: {len(bulk_data['players'])}")
    print(f"Scheduled Games: {len(bulk_data['schedule'])}")

if __name__ == "__main__":
    main()