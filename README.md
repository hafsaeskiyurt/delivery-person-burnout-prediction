# Predictive Burnout Modeling for Delivery Riders:

## ⚠️ The Human Cost of Logistics: The Efficiency Paradox

In the relentless race for “faster” and “cheaper,” the food delivery market has entered a growing Efficiency Paradox. Delivery platforms increasingly rely on algorithmic systems to optimize speed, dispatching, route efficiency, and cost; however, these systems often remain “human-blind,” treating riders as operational variables rather than human workers with physiological and psychological limits. Recent rider-specific research shows why this matters. A 2025 survey of 953 food delivery riders found that burnout is widespread, with 73.9% experiencing moderate burnout and 21.9% experiencing high burnout. In a UK gig-economy survey, 47% of drivers and riders said time pressure could make them travel over the speed limit, and 30% reported running a red light under pressure. Beyond safety, job insecurity also affects workforce stability; recent UK research found that 75% of riders and drivers reported anxiety over potential income drops, while many spent unpaid time waiting for work through the app. For delivery companies, these are not only worker well-being issues. Fatigue, stress, and unsafe time pressure can translate into higher turnover, repeated recruitment and training costs, service-quality problems, accident exposure, and lower operational resilience. In other words, ignoring rider burnout may create short-term efficiency gains while increasing long-term workforce and operational costs.

📍 This project is an AI-driven Decision Support System (DSS) designed to reduce delivery rider burnout risk and support more sustainable last-mile operations. By combining machine learning with industrial engineering principles, the system helps managers make workload-aware assignment decisions that consider not only delivery efficiency but also rider well-being and human-resource sustainability.


## 📊 Dataset
This project uses synthetically generated logistics data to simulate delivery rider burnout risk. The target variable, Burnout_Score, is created using a rule-based formulation that combines shift duration, workload, traffic density, delivery delay, floor level, and elevator availability. Therefore, the model should be interpreted as a proof-of-concept Decision Support System rather than a clinically or operationally validated burnout prediction tool.

## 🛠️ Machine Learning Methodology
- **Model Choice:** Random Forest Regressor
  - While I tested multiple models, the Random Forest Regressor was selected as the core engine.

 
- **Feature Scaling:**
  - Feature scaling (like StandardScaler or MinMaxScaler) was not applied.

    *The Reason:* Random Forest is an ensemble of Decision Trees. Unlike algorithms such as SVM or K-Nearest Neighbors, Tree-based models are scale-invariant. They split data based on thresholds, so the magnitude of the features (e.g., Shift Hour vs. Cumulative Deliveries) does not negatively impact the model's accuracy. Skipping unnecessary scaling keeps the model more interpretable and faster to deploy. Why? Logistics data is often non-linear and complex. Random Forest excels at capturing interactions between features (e.g., how the lack of an elevator in a high-floor building increases burnout faster than just a long shift). It achieved a significantly higher R<sup>2</sup> score (~0.92) compared to Linear Regression.


- **Error Metric:** RMSE over MAE
  - I prioritized Root Mean Squared Error (RMSE) for evaluating model performance.

    *The Reason:* In a human-centric system, large errors are much more dangerous than small ones. RMSE penalizes large outliers more heavily than Mean Absolute Error (MAE). If the model significantly underestimates a rider's burnout, it could lead to an unsafe assignment. RMSE ensures we minimize these high-risk errors to protect our staff.

The model explains about 95.17% of the variation in burnout scores. (R<sup>2</sup> Score) This indicates a very strong fit. On average, the model’s predictions are about 4.42 burnout-score points away from the actual values. (RMSE)

| Model | R<sup>2</sup> Score | RMSE |
| :--- | :--- | :--- |
| Random Forest | 0.9517 | 4.42 |
| Linear Regression | 0.7860 | 9.31 |


- The model is trained on the following features to predict the burnout risk of a rider:

  `Shift_Hour:` The hour of the day the delivery is being made (capturing circadian rhythms and peak fatigue hours).

  `Cumulative_Deliveries:` Total number of deliveries completed by the rider in the current shift.

  `Has_Elevator:` A binary indicator (0 or 1) representing whether the delivery location has an elevator.

  `Building_Floor:` The specific floor level of the delivery address.

  `Delay_From_Target_Min:` The current time pressure, measured as minutes behind or ahead of the scheduled delivery time.

  `Traffic_Density_Low:` One-hot encoded variable representing low traffic conditions.

  `Traffic_Density_Medium:` One-hot encoded variable representing moderate traffic conditions.

## Feature Importance Table

The feature importance chart shows which operational variables had the strongest influence on the predicted burnout score.

<img width="2366" height="1468" alt="image" src="https://github.com/user-attachments/assets/c5e9c3b8-7887-4703-8808-da6b9d2c902d" />


## 🖥️ User Interface (Gradio UI)
I built an interface using **Gradio** to transform a complex backend model into a functional, real-time Decision Support System (DSS). The dashboard allows non-technical individuals to input operational variables—such as building floor, elevator availability, and time pressure—and instantly receive an AI-optimized rider recommendation. By visualizing the "burnout score" ranking, it transforms predictive data into a clear, actionable tool for sustainable labor management.

<img width="1918" height="783" alt="image" src="https://github.com/user-attachments/assets/15d6737b-73c8-460a-aafe-8a0077bffd27" />



## How to Run the Project

This repository does not include the trained model file (`burnout_rf_model.pkl`) due to file size limitations.  
You can generate the model locally by running the training script.

### 1. Clone the Repository

```bash
git clone https://github.com/hafsaeskiyurt/delivery-person-burnout-prediction.git
cd delivery-person-burnout-prediction
```

### 2. Create a Virtual Environment
For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

For macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Libraries
```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, install the required libraries manually:

```bash
pip install pandas numpy scikit-learn joblib gradio matplotlib
```

### 4. Train the Model
Run the training script to train the Random Forest Regressor and generate the model file:
```bash
python train_model.py
```

After running this command, the following file will be created locally:

```text
burnout_rf_model.pkl
```

❗ This file is required for the Gradio application.

### 5. Run the Gradio Application
```bash
python app.py
```

After running the command, Gradio will provide a local URL similar to:
```text
http://127.0.0.1:7860
```

Open this URL in your browser to use the burnout prediction interface.

---

## Project Workflow

```text
courier_data.csv
        ↓
train_model.py
        ↓
burnout_rf_model.pkl
        ↓
app.py
        ↓
Gradio Decision Support Interface
```

---





### 📚 References
- Dong, J., Zhang, G., & Wu, L. (2025). *Life against algorithmic management: a study on burnout and its influencing factors among food delivery riders*. Frontiers in Public Health, 13:1531541.  
  https://doi.org/10.3389/fpubh.2025.1531541

- Christie, N., & Ward, H. (2018). *The emerging issues for management of occupational road risk in a changing economy: A survey of gig economy drivers, riders and their managers*. UCL Centre for Transport Studies.  
  https://discovery.ucl.ac.uk/id/eprint/10057417/

- University of Cambridge. (2025). *Riders and drivers in the UK gig economy suffer anxiety over ratings and pay*.  
  https://www.cam.ac.uk/stories/gig-economy-anxiety-ratings-pay
