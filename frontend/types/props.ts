// types/props.ts
export enum PropCategory {
  POINTS = 'POINTS',
  REBOUNDS = 'REBOUNDS',
  ASSISTS = 'ASSISTS',
  STEALS = 'STEALS',
  BLOCKS = 'BLOCKS',
  THREES = 'THREES'
}

export enum PropType {
  OVER = 'OVER',
  UNDER = 'UNDER'
}

export interface Odds {
  bookmaker: string;
  propType: PropType;
  value: number;
  probability: number;
}

export interface PropBet {
  id: string;
  playerId: string;
  playerName: string;
  sport: string;
  category: PropCategory;
  value: number;
  probability: number;
  recommendedOdds: number;
  odds: Odds[];
  timestamp: string;
  valueIndicator: 'high' | 'medium' | 'low';
  riskScore: number;
}

export interface PlayerStat {
  playerId: string;
  playerName: string;
  category: PropCategory;
  value: number;
  season: number;
  gameLog?: {
    date: string;
    opponent: string;
    statValue: number;
  }[];
  historicalAverage?: number;
  consistency?: number; // Standard deviation or other consistency metric
  recentTrend?: 'rising' | 'falling' | 'stable';
  homeAwayPerformance?: {
    home: number;
    away: number;
  };
}

export interface Odds {
  bookmaker: string;
  propType: PropType;
  value: number;
  probability: number;
}

export interface CustomProp {
  id: string;
  playerId: string[];
  playerName: string;
  categories: PropCategory[];
  combinedValue: number;
  multiplier: number;
  probability: number;
  potentialPayout: number;
  options: string[];
  createdAt: string;
}

export interface PropInsight {
  prop: PropBet;
  sentimentScore: number;
  trendIndicator: 'rising' | 'falling' | 'stable';
  clutchFactor: number;
  fatigueImpact: number;
  recommendedAction: 'bet' | 'avoid' | 'monitor';
}