## Usage
- Install packages
    - `pip install -r requirements.txt`
- You need to have a `drivePath.txt` file, which contains your [chrome drive](https://sites.google.com/chromium.org/driver/), in this repository
- `GetINFO.py` would generate `data.json`, and `UI.py` would take this data to draw someting
- Start
    - `python3 main.py`

## `data.json` Structure
- "teams"
    - "Boston Celtics"
        - "teamData"
            - "PPG": 112.6
            - "RPG": 44.3
            - "APG": 23.5
            - "OPPG": 111.2
        - "playerData":
            - "Jayson Tatum"
                - "NO": 0
                - "POS": "F-G"
                - "HEIGHT": "6-8"
                - "WEIGHT": "210lbs"
                - "AGE": 23
                - "EXP": 3
            - "Carsen Edwards"
                - ...
    - "Brooklyn Nets"
        - ...
    - ...
