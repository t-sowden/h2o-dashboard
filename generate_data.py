import csv
from datetime import datetime, timedelta
import random
import math

random.seed(42)

# 7 days × 24 hours = 168 rows per location
n_hours = 168
start = datetime(2025, 2, 3, 0, 0, 0)

locations = ['Upstream_River', 'Downstream_Plant']
rows = []

for loc in locations:
    for i in range(n_hours):
        dt = start + timedelta(hours=i)
        hour_of_day = dt.hour + dt.minute / 60

        # 1. DateTime (hourly)
        date_time = dt.strftime('%Y-%m-%d %H:%M:%S')

        # 2. pH: normal around 7.2, clip to realistic range
        ph = max(6.5, min(8.5, random.gauss(7.2, 0.3)))
        ph = round(ph, 2)

        # 3. Temp_C: sinusoidal day/night, 10–25°C (peak ~14:00)
        temp_c = 17.5 + 7.5 * math.sin(2 * math.pi * (hour_of_day - 6) / 24)
        temp_c += random.gauss(0, 0.5)
        temp_c = max(10, min(25, round(temp_c, 2)))

        # 4. Turbidity_NTU: mostly 0–5, occasional spike up to 50
        if random.random() < 0.92:
            turbidity = max(0, random.gauss(2, 1.5))
        else:
            turbidity = random.uniform(15, 50)
        turbidity = round(max(0, min(50, turbidity)), 2)

        # 5. DO_mgL: inverse to temperature, range 6–10 (cooler = higher DO)
        do_base = 10 - (temp_c - 10) * (4 / 15)
        do_mgl = do_base + random.gauss(0, 0.2)
        do_mgl = round(max(6, min(10, do_mgl)), 2)

        # 6. Flow_cfs: random variation 45–55
        flow_cfs = round(random.uniform(45, 55), 2)

        rows.append({
            'Location': loc,
            'DateTime': date_time,
            'pH': ph,
            'Temp_C': temp_c,
            'Turbidity_NTU': turbidity,
            'DO_mgL': do_mgl,
            'Flow_cfs': flow_cfs
        })

fieldnames = ['Location', 'DateTime', 'pH', 'Temp_C', 'Turbidity_NTU', 'DO_mgL', 'Flow_cfs']
with open('water_data.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to water_data.csv")
