import { Component, OnInit, OnDestroy } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Subscription } from 'rxjs';
import { PositionSchema } from './position.model';
import { WebSocketService, MarketData } from './web-socket.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'Quant Risk Dashboard';
  positions: Map<string, PositionSchema> = new Map();
  marketDataSubscription: Subscription;
  
  private restApiUrl = 'http://localhost:8000/positions';

  constructor(
    private http: HttpClient,
    public wsService: WebSocketService
  ) {}

  ngOnInit(): void {
    this.fetchInitialPositions();
    this.startRealTimeUpdates();
  }

  fetchInitialPositions(): void {
    this.http.get<PositionSchema[]>(this.restApiUrl).subscribe(
      data => {
        data.forEach(p => this.positions.set(p.symbol, p));
        console.log('Initial Positions Loaded:', this.positions);
      },
      error => console.error('Error fetching positions:', error)
    );
  }

  startRealTimeUpdates(): void {
    this.marketDataSubscription = this.wsService.getMarketData().subscribe(
      (update: MarketData) => {
        const position = this.positions.get(update.symbol);
        
        if (position) {
          // Update all three real-time fields
          position.market_price = update.price;
          position.mtm_pnl = update.pnl;
          position.historical_var_95 = update.var; 
          
          this.positions.set(update.symbol, position);
          this.positions = new Map(this.positions); // Trigger change detection
        }
      },
      error => console.error('Real-time stream error:', error),
      () => console.log('Real-time stream complete')
    );
  }
  
  get positionArray(): PositionSchema[] {
    return Array.from(this.positions.values());
  }

  ngOnDestroy(): void {
    if (this.marketDataSubscription) {
      this.marketDataSubscription.unsubscribe();
    }
  }
}