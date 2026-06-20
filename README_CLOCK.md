# 🕐 Digital Clock - Multiple Time Zones

A modern web-based and console-based digital clock that displays current time in different time zones around the world.

## Features

✨ **Real-time Updates** - Updates every second with live time information  
✨ **12 Global Time Zones** - Displays time from major cities worldwide  
✨ **Multiple Interfaces**:
  - 🌐 **Web Interface** - Beautiful responsive web app
  - 💻 **Console Clock** - Terminal-based display
  - 🐍 **Python Module** - Programmatic access

✨ **Interactive Features**:
  - 24-hour and 12-hour time format toggle
  - Analog clock visualization
  - Sort clocks by time
  - UTC offset information
  - Date and timezone display
  - Responsive design (works on mobile, tablet, desktop)

✨ **Supported Time Zones**:
  - 🗽 New York (America/New_York)
  - 🇬🇧 London (Europe/London)
  - 🗻 Tokyo (Asia/Tokyo)
  - 🦘 Sydney (Australia/Sydney)
  - 🏙️ Dubai (Asia/Dubai)
  - 🇸🇬 Singapore (Asia/Singapore)
  - 🇭🇰 Hong Kong (Asia/Hong_Kong)
  - 🇮🇳 Mumbai (Asia/Kolkata)
  - 🇩🇪 Berlin (Europe/Berlin)
  - 🇧🇷 São Paulo (America/Sao_Paulo)
  - 🌴 Los Angeles (America/Los_Angeles)
  - 🇹🇭 Bangkok (Asia/Bangkok)

## Installation

```bash
pip install -r clock_requirements.txt
```

## Usage

### 1. Web Interface

```bash
# Start Flask server
python app.py

# Open browser and visit
http://localhost:5000
```

**Features:**
- Beautiful gradient background
- Animated cards with hover effects
- Real-time updates
- Toggle between 24h and 12h format
- Analog and digital clocks
- Responsive grid layout

### 2. Console Clock

```bash
python console_clock.py
```

**Features:**
- Live updating terminal display
- Box-drawn interface
- Clean formatting
- Real-time updates every second

### 3. Python Module

```python
from digital_clock import TimeZoneClock

# Create clock instance
clock = TimeZoneClock()

# Get all times
all_times = clock.get_all_times()

# Get time for specific timezone
ny_time = clock.get_time_in_zone('America/New_York')

# Get formatted display
print(clock.get_formatted_display())
```

## API Endpoints

### Get All Times
```
GET /api/time
```
Returns JSON with current time in all configured time zones

### Get Time for Specific City
```
GET /api/time/<city>
```
Example: `/api/time/New%20York`

### Add New Timezone
```
GET /api/add-timezone/<city>/<timezone>
```
Example: `/api/add-timezone/Paris/Europe%2FParis`

## Response Format

```json
{
  "New York": {
    "time": "14:30:45",
    "time_12h": "02:30:45 PM",
    "date": "Friday, June 20, 2024",
    "timezone": "EDT",
    "offset": "-0400",
    "hour": 14,
    "minute": 30,
    "second": 45
  }
}
```

## Customization

### Add Custom Time Zones

**In Python:**
```python
from digital_clock import TimeZoneClock

custom_zones = {
    'Paris': 'Europe/Paris',
    'Moscow': 'Europe/Moscow',
    'Beijing': 'Asia/Shanghai',
}

clock = TimeZoneClock(time_zones=custom_zones)
```

**In Web App:**
Visit `/api/add-timezone/CityName/Timezone`

### Modify Styles

Edit `templates/clock.html` CSS section to customize:
- Colors
- Layout
- Fonts
- Animations

## Technical Details

### Technologies Used
- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Timezone Library**: pytz
- **Time Management**: Python datetime module

### Browser Support
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers

### Performance
- Real-time updates every 1 second
- Lightweight API responses
- Optimized CSS animations
- Responsive grid layout

## File Structure

```
📁 Clock Project
├── app.py                 # Flask web application
├── digital_clock.py       # Core timezone clock class
├── console_clock.py       # Terminal-based clock
├── clock_requirements.txt  # Dependencies
├── templates/
│   └── clock.html         # Web interface
└── README_CLOCK.md       # This file
```

## Examples

### Get current time in all zones
```python
from digital_clock import TimeZoneClock
clock = TimeZoneClock()
times = clock.get_all_times()
for city, info in times.items():
    print(f"{city}: {info['time']}")
```

### Create a simple CLI timer
```python
from digital_clock import TimeZoneClock
import time

clock = TimeZoneClock()
for _ in range(10):
    print(clock.get_formatted_display())
    time.sleep(1)
```

## Timezone Reference

Complete list of available timezones: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

Common timezone strings:
- `America/New_York` - Eastern Time
- `Europe/London` - Greenwich Mean Time
- `Asia/Tokyo` - Japan Standard Time
- `Australia/Sydney` - Australian Eastern Time
- `Pacific/Auckland` - New Zealand Standard Time

## Troubleshooting

### Clock not updating
- Check if JavaScript is enabled in browser
- Verify Flask server is running (`python app.py`)
- Check browser console for errors (F12)

### Wrong time displayed
- Ensure system time is correct
- Check timezone setting in operating system
- Verify pytz database is up to date

### 404 Error on API calls
- Ensure city name matches exactly (case-sensitive in API)
- URL encode special characters (e.g., space = %20)

## License

Educational use - Free to modify and distribute

---

**Happy time tracking!** ⏰🌍
