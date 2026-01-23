import pandas as pd
from sklearn.ensemble import IsolationForest
import re

LOG_FILE = "../logs/system_logs.txt"

# Step 1: Read logs
logs = []
with open(LOG_FILE, "r") as file:
    for line in file:
        match = re.match(r"(.*) (INFO|WARNING|ERROR|CRITICAL) (.*)", line)
        if match:
            timestamp, level, message = match.groups()
            logs.append([timestamp, level, message])

df = pd.DataFrame(logs, columns=["timestamp", "level", "message"])
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Step 2: Feature Engineering
level_mapping = {"INFO": 1, "WARNING": 2, "ERROR": 3, "CRITICAL": 4}
df["level_score"] = df["level"].map(level_mapping)
df["message_length"] = df["message"].apply(len)

# Step 3: AI Model
model = IsolationForest(contamination=0.15, random_state=42)
df["anomaly_score"] = model.fit_predict(
    df[["level_score", "message_length"]]
)

# Step 4: Human-readable output
df["status"] = df["anomaly_score"].apply(
    lambda x: "Anomaly" if x == -1 else "Normal"
)

# Step 5: Output results
print("\n AI-Driven Log Anomaly Detection Results:\n")
print(df[["timestamp", "level", "message", "status"]])

print("\n Detected Anomalies:\n")
print(df[df["status"] == " Anomaly"])
