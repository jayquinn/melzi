import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'config.json')

DEFAULT_CONFIG = {
  "min_wage": 9860,
  "overtime_rate": 1.5,
  "meal_tax_free_limit": 200000,
  "family_allowance_per_person": 100000,
  "zombie_months": 3,
  "bottleneck_limit": 15,
  "ghost_shift_tolerance": 60,
  "notification_schedule": ["D-5", "D-3", "D-1"],
  "vip_filter": ["Executive", "Team Lead"],
  "msg_template": "안녕하세요 {name}님, 급여 마감을 위해 확인 부탁드립니다."
}

def load_config():
    """Loads configuration from JSON file. Returns default if file missing."""
    if not os.path.exists(CONFIG_PATH):
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return DEFAULT_CONFIG.copy()

def save_config(new_config):
    """Saves configuration to JSON file."""
    try:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(new_config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

def reset_config():
    """Resets configuration to default values."""
    save_config(DEFAULT_CONFIG)
    return DEFAULT_CONFIG.copy()
