import json
import random
from datetime import datetime, timedelta, timezone
from bson import ObjectId

def generate_random_float(min_val, max_val, decimals=2):
  return round(random.uniform(min_val, max_val), decimals)

def generate_random_timestamp(start_date, end_date):
  time_between = end_date - start_date
  random_seconds = random.randint(0, int(time_between.total_seconds()))
  return start_date + timedelta(seconds=random_seconds)

# Generate data list
total_data = 2000
# Bulan Agustus 2025 (1-31 Agustus 2025)
start = datetime(2025, 8, 1, tzinfo=timezone.utc)
end = datetime(2025, 8, 31, 23, 59, 59, tzinfo=timezone.utc)

# Generate data list
data_list = []
for i in range(total_data):
  timestamp = generate_random_timestamp(start, end)
  data = {
    "suhu": generate_random_float(20, 35),
    "ph": generate_random_float(6.5, 8.5),
    "tds": generate_random_float(100, 1000),
    "turbidity": generate_random_float(0, 100),
    "timestamp": {"$date": timestamp.isoformat()}
  }
  data_list.append(data)

# Export untuk MongoDB import (NDJSON)
with open("sensor_data_mongoimport.json", "w") as f:
  for item in data_list:
    f.write(json.dumps(item) + '\n')

print("✅ sensor_data_mongoimport.json generated")
print("   Import dengan: mongoimport --db nilo --collection sensor --file sensor_data_mongoimport.json")
print(f"📊 Total data generated: {total_data}")
