import gradio as gr
import joblib
import pandas as pd
import numpy as np
import random

# 1. LOAD THE TRAINED BRAIN
# We load the 'knowledge' the model gained during the training phase.
# This file contains all the decision trees for predicting burnout.
try:
    rf_model = joblib.load('burnout_rf_model.pkl')
    print(">>> AI Engine successfully loaded.")
except FileNotFoundError:
    print(">>> Error: 'burnout_rf_model.pkl' not found. Please ensure it is in the same folder.")

# 2. DEFINE THE MUNICH LOGISTICS NETWORK
# Setting up our 10 operation districts in Munich.
munich_regions = [
    "Altstadt", "Maxvorstadt", "Schwabing", "Ludwigsvorstadt", "Sendling", 
    "Isarvorstadt", "Au-Haidhausen", "Bogenhausen", "Pasing", "Laim"
]

# 3. GENERATE SYNTHETIC RIDER DATABASE
# Creating a pool of riders distributed across Munich to test the "Optimal Match" logic.
def generate_riders():
    riders = []
    for region in munich_regions:
        # Assign 10 to 16 riders per district to simulate real-world staffing.
        num_riders = random.randint(10, 16)
        for i in range(num_riders):
            riders.append({
                "Rider_ID": f"{region[:3].upper()}-{i+100}", # e.g., SCH-101
                "Region": region,
                "Shift_Hour": random.randint(1, 8),           # Current time into shift
                "Cumulative_Deliveries": random.randint(5, 25)# Workload handled today
            })
    return pd.DataFrame(riders)

# Initialize the rider database in memory
rider_database = generate_riders()

# 4. CORE DISPATCH LOGIC (Decision Support System)
def smart_dispatch_logic(order_region, has_elevator, floor, delay, traffic):
    # Filter only the riders currently located in the order's specific region.
    local_candidates = rider_database[rider_database['Region'] == order_region].copy()
    
    simulation_results = []
    
    # "What-If" Analysis: Test this specific order against every local rider.
    for _, rider in local_candidates.iterrows():
        # Build the feature matrix for the model
        test_case = pd.DataFrame([{
            'Shift_Hour': rider['Shift_Hour'],
            'Cumulative_Deliveries': rider['Cumulative_Deliveries'],
            'Has_Elevator': 1 if has_elevator == "Yes" else 0,
            'Building_Floor': floor,
            'Delay_From_Target_Min': delay,
            'Traffic_Density_Low': 1 if traffic == "Low" else 0,
            'Traffic_Density_Medium': 1 if traffic == "Medium" else 0
        }])
        
        # Ensure column order matches the model's original training structure.
        test_case = test_case[rf_model.feature_names_in_]
        
        # Calculate the predicted burnout score for this specific rider-order pair.
        prediction = rf_model.predict(test_case)[0]
        simulation_results.append(prediction)
    
    local_candidates['Predicted_Burnout'] = simulation_results
    
    # INDUSTRIAL ENGINEERING OPTIMIZATION:
    # Filter candidates below the safety threshold (85) and find the one with the lowest score.
    safe_candidates = local_candidates[local_candidates['Predicted_Burnout'] < 85]
    
    if not safe_candidates.empty:
        # Find the most "rested/fresh" rider for this specific task.
        best_match = safe_candidates.loc[safe_candidates['Predicted_Burnout'].idxmin()]
        
        summary = f"🏆 OPTIMAL MATCH: {best_match['Rider_ID']}\n"
        summary += f"Estimated Burnout Score: {best_match['Predicted_Burnout']:.2f}\n"
        summary += f"Status: Rider is at hour {best_match['Shift_Hour']} of shift with {best_match['Cumulative_Deliveries']} deliveries completed."
    else:
        # If every rider in the district is too exhausted, alert the manager.
        summary = "🚨 OPERATION ALERT: No safe riders available in this district. High risk of labor turnover if assigned."

    # Return the top 5 best matches for the UI table
    comparison_table = local_candidates[['Rider_ID', 'Predicted_Burnout']].sort_values(by='Predicted_Burnout').head(5)
    return summary, comparison_table

# 5. GRADIO UI CONFIGURATION
with gr.Blocks() as dispatch_app:
    gr.Markdown("# 🚀 Smart Logistics Dispatcher - Munich Hub")
    gr.Markdown("Real-time AI assignment system to prevent rider burnout and optimize labor retention.")
    
    with gr.Row():
        # LEFT COLUMN: Order Details (Input)
        with gr.Column():
            gr.Markdown("### 📦 Delivery Details")
            region_input = gr.Dropdown(munich_regions, label="Delivery District")
            elev_input = gr.Radio(["Yes", "No"], label="Elevator in Building?")
            floor_input = gr.Slider(0, 10, label="Target Floor Level")
            delay_input = gr.Slider(-10, 20, label="Expected Delay Pressure (Min)", info="Negative: Early delivery | 0: On-time | Positive: Late delivery")
            traffic_input = gr.Dropdown(["Low", "Medium", "High"], label="Current Traffic Density")
            
            submit_btn = gr.Button("Calculate Optimal Assignment", variant="primary")
            
        # RIGHT COLUMN: AI Analysis (Output)
        with gr.Column():
            gr.Markdown("### 🤖 AI Dispatch Decision")
            final_decision = gr.Textbox(label="Assignment Recommendation", lines=4)
            data_table = gr.Dataframe(label="Candidate Ranking (Top 5)")

    # LINK THE BUTTON TO THE LOGIC
    submit_btn.click(
        fn=smart_dispatch_logic, 
        inputs=[region_input, elev_input, floor_input, delay_input, traffic_input], 
        outputs=[final_decision, data_table]
    )

# 6. LAUNCH THE INTERFACE
# This will open a local web server (http://127.0.0.1:7860)
dispatch_app.launch()