import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { Observable } from 'rxjs';

// Define the shape of the real-time data
export interface MarketData {
  symbol: string;
  price: number;
  pnl: number;           // P&L update
  var: number;           // VaR update
}

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {
  private marketDataUrl = 'ws://localhost:8000/ws/market_data';
  public socket$: WebSocketSubject<MarketData>; // Make public for status check in template

  constructor() {
    this.connect();
  }

  private connect(): void {
    this.socket$ = webSocket<MarketData>(this.marketDataUrl);
    
    this.socket$.subscribe({
      next: (msg) => console.log('Market Update Received:', msg),
      error: (err) => console.error('WebSocket Error:', err),
      complete: () => console.log('WebSocket Connection Closed')
    });
  }

  public getMarketData(): Observable<MarketData> {
    return this.socket$.asObservable();
  }
}