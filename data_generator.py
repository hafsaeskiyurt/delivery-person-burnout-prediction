import pandas as pd
import numpy as np
import uuid

# Set random seed for reproducibility of human behaviors
np.random.seed(42)

num_records = 10000

# Generate a static pool of 150 active delivery riders
rider_pool = [f"RIDER_{i:03d}" for i in range(1, 151)]
assigned_riders = np.random.choice(rider_pool, size=num_records)

# Simulate raw operational logistics data structure
data = {
    'Delivery_ID': [str(uuid.uuid4())[:8] for _ in range(num_records)],
    'Rider_ID': assigned_riders,
    'Shift_Hour': np.random.randint(1, 11, size=num_records), 
    'Cumulative_Deliveries': np.random.randint(1, 25, size=num_records), 
    'Has_Elevator': np.random.choice([1, 0], size=num_records, p=[0.65, 0.35]), 
    'Building_Floor': np.random.randint(0, 11, size=num_records), 
    'Traffic_Density': np.random.choice(['Low', 'Medium', 'High'], size=num_records, p=[0.3, 0.5, 0.2]),
    'Delay_From_Target_Min': np.random.normal(loc=2.0, scale=4.0, size=num_records).round(1) 
}

df = pd.DataFrame(data)

# Logic fix: Elevator presence does not matter if delivery is on the ground floor (Floor 0)
df.loc[df['Building_Floor'] == 0, 'Has_Elevator'] = 1

# Mathematical Formulation of Human Behavior (The Burnout Engine)
def calculate_burnout_score(row):
    # Base physiological baseline stress
    score = 15 
    
    # Fatigue accumulation over time and workload
    score += row['Shift_Hour'] * 4.5
    score += row['Cumulative_Deliveries'] * 1.2
    
    # Heavy physical penalty: Walking up stairs on high floors without an elevator
    if row['Has_Elevator'] == 0 and row['Building_Floor'] > 2:
        score += row['Building_Floor'] * 6.5
        
    # Mental/environmental cognitive load from city traffic
    if row['Traffic_Density'] == 'High':
        score += 20
    elif row['Traffic_Density'] == 'Medium':
        score += 8
        
    # Psychological time-pressure anxiety (capped at max 25 points penalty)
    if row['Delay_From_Target_Min'] > 0:
        score += min(row['Delay_From_Target_Min'] * 1.5, 25) 
        
    # Add Gaussian white noise to simulate unpredictable human psychology/mood
    score += np.random.normal(0, 4)
    
    # Constrain the target variable mathematically between 0 and 100
    return int(np.clip(score, 0, 100))

# Execute the behavior calculation matrix across the dataframe
df['Burnout_Score'] = df.apply(calculate_burnout_score, axis=1)

# Export the generated synthetic data asset to disk
df.to_csv('courier_burnout_data.csv', index=False)
print(f"Success! 'courier_burnout_data.csv' generated with {df.shape[0]} rows.")