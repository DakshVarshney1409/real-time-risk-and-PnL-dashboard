export interface PositionSchema {
    symbol: string;
    quantity: number;
    average_cost: number;
    market_price: number;
    mtm_pnl: number;           
    historical_var_95: number; 
  }