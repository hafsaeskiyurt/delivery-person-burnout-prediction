### ⚠️ The Human Cost of Logistics: The Efficiency Paradox

In the relentless race for **"faster"** and **"cheaper,"** the global delivery market has stumbled into a dangerous **Efficiency Paradox**. While modern algorithms are masterfully optimized to shave off milliseconds and cents, they remain fundamentally "human-blind," *treating riders as static variables* rather than biological assets. This oversight has fueled a silent crisis: **a 70% to 100% annual turnover rate** that traps firms in a "revolving door" of recruitment, costing upwards of €5,000 per rider in lost productivity and training. Beyond the financial drain, the psychological toll is immense, **with 63% of riders reporting high distress**. When a system ignores the cumulative mental fatigue of its workforce, it doesn't just lose money—it inadvertently forces its most efficient people into a "death spiral" of burnout, ultimately destabilizing the entire supply chain and tripling the risk of operational accidents. 

📍 This project is an AI-driven Decision Support System (DSS) designed to combat rider burnout and high labor turnover rates in the logistics sector. By integrating Machine Learning with industrial engineering principles, the system ensures sustainable delivery operations by prioritizing human resources.

### 🛠️ Machine Learning Methodology
- **Model Choice:** Random Forest Regresson
  - While I tested multiple models, the Random Forest Regressor was selected as the core engine.

 
- **Feature Scaling:**
  - You might notice that I did not apply Feature Scaling (like StandardScaler or MinMaxScaler).

    The Reason: Random Forest is an ensemble of Decision Trees. Unlike algorithms such as SVM or K-Nearest Neighbors, Tree-based models are scale-invariant. They split data based on thresholds, so the magnitude of the features (e.g., Shift Hour vs. Cumulative Deliveries) does not negatively impact the model's accuracy. Skipping unnecessary scaling keeps the model more interpretable and faster to deploy. Why? Logistics data is often non-linear and complex. Random Forest excels at capturing interactions between features (e.g., how the lack of an elevator in a high-floor building increases burnout faster than just a long shift). It achieved a significantly higher R<sup>2</sup> score (~0.92) compared to Linear Regression.


- **Error Metric:** RMSE over MAE
  - I prioritized Root Mean Squared Error (RMSE) for evaluating model performance.

  The Reason: In a human-centric system, large errors are much more dangerous than small ones. RMSE penalizes large outliers more heavily than Mean Absolute Error (MAE). If the model significantly underestimates a rider's burnout, it could lead to an unsafe assignment. RMSE ensures we minimize these high-risk errors to protect our staff.



| Metric | Result | Meaning |
| :--- | :--- | :--- |
| R2 Score | ~0.92 | The model explains 92% of the variance in burnout scores. |
| RMSE | ~2.1 points | On average, the prediction only deviates by ~2 points on a 100-point scale. |


- The model is trained on the following features to predict the burnout risk of a rider:

  Shift_Hour: The hour of the day the delivery is being made (capturing circadian rhythms and peak fatigue hours).

  Cumulative_Deliveries: Total number of deliveries completed by the rider in the current shift.

  Has_Elevator: A binary indicator (0 or 1) representing whether the delivery location has an elevator.

  Building_Floor: The specific floor level of the delivery address.

  Delay_From_Target_Min: The current time pressure, measured as minutes behind or ahead of the scheduled delivery time.

  Traffic_Density_Low: One-hot encoded variable representing low traffic conditions.

  Traffic_Density_Medium: One-hot encoded variable representing moderate traffic conditions.

### 🖥️ User Interface (Gradio UI)
I built an interface using **Gradio** to transform a complex backend model into a functional, real-time Decision Support System (DSS). The dashboard allows non-technical individuals to input operational variables—such as building floor, elevator availability, and time pressure—and instantly receive an AI-optimized rider recommendation. By visualizing the "burnout score" ranking, it transforms predictive data into a clear, actionable tool for sustainable labor management.

<img width="1918" height="783" alt="image" src="https://github.com/user-attachments/assets/15d6737b-73c8-460a-aafe-8a0077bffd27" />



## 🚀 Getting Started
1. Installation
   Open your terminal and run the following command to install all necessary libraries:

   ` pip install gradio pandas joblib scikit-learn numpy `

3. File Requirements
   Make sure the following files are in the same directory:

   ` app.py ` (The main application script), ` burnout_rf_model.pkl ` (The trained AI model)

5. Running the App
   Execute the following command in your terminal:

   ` python app.py `

👉 Once the script is running, the terminal will provide a local URL. Copy and paste this address into your web browser to access the dashboard.


### 📚 References

- World Economic Forum (2020): “The Future of the Last Mile Ecosystem”
- Eurofound (2021): “Occupational Safety and Health in the Platform Economy”
- Journal of Business Research: “The Impact of Time Pressure and Fatigue on Gig Worker Performance”
- Statista (2023): “Logistics Personnel Turnover Trends in Europe”
