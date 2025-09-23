# Trading Forecast Bot  

A modular, event-driven trading forecast bot built with **Selenium**, **ByBit API**, **SQLAlchemy**, and **schedule**.  
The project follows a **Clean Architecture** approach with clear separation of concerns across domain, infrastructure, service, and entrypoint layers.

## ⚡ Features  

- **Trading Data Collection** – scheduled fetching of candles, indicators, and signals  
- **Forecast Generation** – integrates with **OpenAI** to provide text-based market forecasts  
- **Multi-Exchange Ready** – modular clients (e.g., Bybit, TradingView)  
- **Clean Architecture** – decoupled layers for maintainability and scalability  
- **Persistence** – PostgreSQL database with SQLAlchemy ORM
- **Task Scheduling**