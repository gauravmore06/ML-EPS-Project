# 🚀 ML-EPS-Project

## 📖 About the Project  

Industrial equipment often produces **sensor data** that indicates the **health status of machines**.  
Predicting potential failures early can:  

⚡ **Reduce downtime**  
⚙️ **Improve maintenance efficiency**  
💰 **Save operational costs**  

🔍 This project demonstrates how to:  

1️⃣ Ingest raw sensor data from **CSV** or **database**  
2️⃣ **Preprocess & clean** data → handle missing values, scaling, transformations  
3️⃣ Train **ML models** → (classification: *faulty* vs. *healthy* machine state)  
4️⃣ **Save & load** the latest best model automatically  
5️⃣ Expose **REST APIs** for:  

- 🏋️ **Training** → `/train`  
- 🔮 **Prediction** → `/predict`  

✨ The project is designed with **scalability in mind** → you can plug in new datasets, retrain models, and serve predictions without changing the core codebase.  

---

## 📝 Problem Statement  

**📊 Data Source:** Sensor Data  

The system in focus is the **Air Pressure System (APS)**, which generates pressurized air used in critical truck functions such as **braking** and **gear changes**.  

- ✅ The **positive class** corresponds to **component failures** for a specific APS component.  
- ❌ The **negative class** corresponds to **trucks with failures unrelated to the APS system**.  

### 🎯 Objective  
The main goal is to **reduce the cost of unnecessary repairs** by building a predictive system that:  

- Minimizes **false positives** (predicting a failure when there is none).  
- Minimizes **false negatives** (missing an actual failure).  
- Improves **maintenance efficiency** while ensuring **safety and reliability** of the trucks.  

---

## 📊 Dataset Overview  

- 📂 **Dataset Type:** Tabular sensor data  
- 🔢 **Features:** ~170 sensor readings (continuous + categorical features)  
- 🧩 **Target Variable:** Binary classification (APS failure → `1`, No failure → `0`)  
- ⚠️ **Challenges:**  
  - Many **missing values**  
  - **Imbalanced classes** (failures are rare compared to normal cases)  
  - Large-scale dataset requiring **efficient preprocessing**  

---

## 📂 Project Structure  

```bash
ML-EPS-Project/
├── artifact/           # 📁 Training artifacts (logs, outputs, checkpoints)
├── config/             # ⚙️ Configuration files
├── saved_models/       # 🧠 Serialized trained models
├── sensor/             # 🏗 Core package (pipeline, configs, utils)
│   ├── pipeline/       # 🔄 Training pipeline
│   ├── configuration/  # 🗄 MongoDB & config helpers
│   ├── ml/             # 🤖 Model utilities (resolver, mappings, estimator)
│   └── utils/          # 🛠 Helper functions
├── main.py             # 🚀 Main FastAPI application
├── fast.py             # ⚡ Alternate FastAPI app (optional)
├── input_file.csv      # 📊 Sample input file for predictions
├── requirements.txt    # 📦 Python dependencies
└── setup.py            # 🛠 Package setup script
