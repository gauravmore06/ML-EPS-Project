## 📖 About the Project  

Industrial equipment often produces sensor data that indicates the health status of machines. Predicting potential failures early can:  

⚡ Reduce downtime  
⚙️ Improve maintenance efficiency  
💰 Save operational costs  

🔍 This project demonstrates how to:  

1️⃣ Ingest raw sensor data from CSV or database  
2️⃣ Preprocess and clean data → handle missing values, scaling, transformations  
3️⃣ Train ML models → (classification: faulty vs. healthy machine state)  
4️⃣ Save & load the latest best model automatically  
5️⃣ Expose REST APIs for:  

- 🏋️ **Training** → `/train`  
- 🔮 **Prediction** → `/predict`  

✨ The project is designed with scalability in mind → you can plug in new datasets, retrain models, and serve predictions without changing the core codebase.  

---

## 📂 Project Structure  

```bash
ML-EPS-Project/
│
├── artifact/            # 📁 Training artifacts (logs, outputs, checkpoints)
├── config/              # ⚙️ Configuration files
├── saved_models/        # 🧠 Serialized trained models
│
├── sensor/              # 🏗 Core package (pipeline, configs, utils)
│   ├── pipeline/        # 🔄 Training pipeline
│   ├── configuration/   # 🗄 MongoDB & config helpers
│   ├── ml/              # 🤖 Model utilities (resolver, mappings, estimator)
│   └── utils/           # 🛠 Helper functions
│
├── main.py              # 🚀 Main FastAPI application
├── fast.py              # ⚡ Alternate FastAPI app (optional)
├── input_file.csv       # 📊 Sample input file for predictions
├── requirements.txt     # 📦 Python dependencies
└── setup.py             # 🛠 Package setup script
