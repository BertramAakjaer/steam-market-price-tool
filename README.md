```bash
 ____   _                             __  __               _           _     _____                _
/ ___| | |_   ___   __ _  _ __ ___   |  \/  |  __ _  _ __ | | __  ___ | |_  |_   _|  ___    ___  | |
\___ \ | __| / _ \ / _` || '_ ` _ \  | |\/| | / _` || '__|| |/ / / _ \| __|   | |   / _ \  / _ \ | |
 ___) || |_ |  __/| (_| || | | | | | | |  | || (_| || |   |   < |  __/| |_    | |  | (_) || (_) || |
|____/  \__| \___| \__,_||_| |_| |_| |_|  |_| \__,_||_|   |_|\_\ \___| \__|   |_|   \___/  \___/ |_|
```

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Steam](https://img.shields.io/badge/Steam-Market-000000.svg?logo=steam)

> A powerful tool for calculating on items in the steam market like CS2 case prices. This includes real-time updates and price caching for limited API calls.

## ✨ Features

- 🔄 Real-time price fetching from Steam Market
- 💰 Support for both median and lowest prices (for bulk purchases)
- ⚡ Price caching system for faster loading
- 📊 Budget calculator for items investments (or gamling 😉)
- 🎯 Track multiple items simultaneously
- 🕒 Automatic price refresh after 1 hour

## 🚀 Installation

1. Clone the repository
```bash
git clone https://github.com/BertramAakjaer/steam-market-price-tool.git

cd steam-market-price-tool
```

2. Install requirements
```bash
pip install -r requirements.txt
```

3. Configure your cases in `config.json`
```json
{
    "case_name": {
        "name": "Display-Name",
        "hash": "Steam-Market-Hash-Name"
    },

    "case_name2": {
        "name": "Display-Name2",
        "hash": "Steam-Market-Hash-Name2"
    }
}
```

## 💻 Usage

Run the main script:
```bash
python main.py
```

### Available Commands:
- `1` - Calculate prices for specific quantities
- `2` - Budget calculator
- `3` - Display current prices
- `4` - Force price recalculation
- `5` - Switch between median/lowest prices
- `6` - Exit

## ⚙️ Configuration

The tool uses `config.json` to manage item configurations. Each item needs:
- `name`: Display name for the case
- `hash`: Steam market hash name (URL encoded)

The name is fully optional and will only be shown to you to keep an eye on each item type.

But the `hash` is important. It can be found in the URL, like here for the Kilowatt-Case, where it would be `"Kilowatt%20Case"`
- [steamcommunity.com/market/listings/730/Kilowatt%20Case](https://steamcommunity.com/market/listings/730/Kilowatt%20Case)

## 🔧 Technical Details

- Price caching system to reduce API calls
- Automatic refresh of prices older than 1 hour
- Error handling for API requests
- Progress bars for loading operations

## 📚 Dependencies

- [requests](https://requests.readthedocs.io/) - HTTP library for API calls
- [tqdm](https://tqdm.github.io/) - Progress bar functionality
- [art](https://github.com/sepandhaghighi/art) - ASCII art generation

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

##  **Socials** 🐦

>  [aakjaer.site](https://www.aakjaer.site) &nbsp;&middot;&nbsp;
>  GitHub [@BertramAakjær](https://github.com/BertramAakjaer) &nbsp;&middot;&nbsp;
>  Twitter [@BertramAakjær](https://twitter.com/BertramAakjaer)
