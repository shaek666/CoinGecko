# 🚀 Crypto Market Intelligence

An automated **[CoinGecko data scraper](https://www.coingecko.com/)** using **Selenium**, processed and cleaned with **Pandas**, and visualized in an **interactive Tableau dashboard**. This project enables efficient tracking of cryptocurrency market trends.

## Table of Contents

- [Introduction](#introduction)
- [Key Findings](#key-findings)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Introduction

Crypto Market Intelligence is a comprehensive tool designed to scrape cryptocurrency data from CoinGecko, process and clean the data using Pandas, and visualize the results in an interactive Tableau dashboard. This project aims to provide users with up-to-date and insightful information about the cryptocurrency market.

## Key Findings

- **Market Capitalization:** Bitcoin and Ethereum clearly lead the market, dominating overall market cap compared to other cryptocurrencies.
- **Price Volatility:** Historical price trends reveal significant fluctuations, underscoring the inherent volatility in crypto markets.
- **Trading Volume:** High trading volumes in key assets highlight liquidity, while smaller coins may experience sharper price swings.
- **Top Gainers/Losers:** The dashboard pinpoints cryptocurrencies with the most notable percentage gains and losses over specific periods.

## Features

- Automated data scraping from CoinGecko using Selenium
- Data cleaning and processing with Pandas
- Interactive data visualization with Tableau
- CSV export of cleaned data for further analysis

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/crypto-market-intelligence.git
    cd crypto-market-intelligence
    ```

2. Set up the virtual environment:
    ```sh
    python -m venv venv
    source venv\Scripts\activate
    ```

3. Install the required dependencies.

4. Download and install the ChromeDriver that matches your Chrome browser version. Update the path to the ChromeDriver in the `setup_driver` function in `coin.py`.

## Usage

1. Run the data scraper:
    ```sh
    python coin.py
    ```

2. Process the scraped data.

3. You can view the interactive dashboard online by visiting the link provided in the `useful_urls.txt` file or directly [here](https://public.tableau.com/views/CryptoMarketIntelligence/CryptocurrencyMarketInsights?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link).


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
