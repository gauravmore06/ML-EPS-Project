📖 About the Project

Industrial equipment often produces sensor data that indicates the health status of machines. Predicting potential failures early can:

⚡ Reduce downtime

⚙️ Improve maintenance efficiency

💰 Save operational costs

This project demonstrates how to:

Ingest raw sensor data from CSV / database

Preprocess and clean data (handle missing values, scaling, transformations)

Train ML models (classification task: faulty vs. healthy machine state)

Save and load the latest best model automatically

Expose APIs for:

Training (/train)

Prediction (/predict)

The project is designed with scalability in mind: you can plug in new datasets, retrain models, and serve predictions without changing the core codebase.
