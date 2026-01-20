POC:  AI MODEL:  

AI-Driven Log Anomaly Detection POC – Full Documentation 

 

1️⃣ Overview 

This POC demonstrates how to integrate an AI model for anomaly detection into a DevOps environment using Python, Docker, and Kubernetes CronJobs. It automatically scans log files for unusual patterns (anomalies) like spikes in errors or critical messages, and flags them for review. 

AI model used: Isolation Forest (unsupervised anomaly detection) 

Log files analyzed: Application logs, system logs, database logs, Kubernetes pod logs 

Automation: CronJob in Kubernetes runs the anomaly detection periodically 

Containerized: Docker image makes it portable and scalable 

 

2️⃣ Benefits for DevOps & AI/ML 

DevOps Benefits: 

Detect unusual spikes in errors before they cause downtime 

Monitor Kubernetes cluster logs, CI/CD pipelines, or microservices logs 

Enables predictive insights, helping to proactively fix issues 

Integrates AI directly into DevOps workflows 

AI/ML Benefits: 

Uses Isolation Forest to automatically identify anomalous log patterns 

Can detect anomalies that human monitoring might miss 

Helps build intelligent monitoring dashboards (Grafana/Slack/Email) 

Can be extended to real-time log streaming (via Fluentd, Elasticsearch, Kafka) 

 

3️⃣ Prerequisites 

Git installed on your machine 

Docker installed 

Minikube installed (for local Kubernetes cluster) 

kubectl installed (Kubernetes CLI) 

Python 3.x (for local testing, optional) 

Basic knowledge of terminal/command line 

 

4️⃣ Project Setup 

4.1 Clone the Repository 

cd ~/Desktop/AI-ML/ 
git clone git@github.com:askafs/afs-anamoly-poc.git 
cd afs-anamoly-poc 
git checkout main 

 

4.2 Create Logs Directory and File 

Create the logs/ folder: 

mkdir logs 
 

Create system_logs.txt: 

nano logs/system_logs.txt 
 

Paste the following logs into the editor: 

2024-01-01 10:00:01 INFO Application started 
2024-01-01 10:00:05 INFO User logged in 
2024-01-01 10:00:10 WARNING High memory usage 
2024-01-01 10:00:15 ERROR Database connection failed 
2024-01-01 10:00:18 ERROR Database connection failed 
2024-01-01 10:00:20 ERROR Database connection failed 
2024-01-01 10:00:22 ERROR Database connection failed 
2024-01-01 10:00:30 INFO Retrying connection 
2024-01-01 10:00:35 CRITICAL Kernel panic detected - unexpected shutdown 
 

Save & exit: 

CTRL + O → Enter (save) 

CTRL + X (exit) 

Verify file: 

ls logs 
cat logs/system_logs.txt 
 

Add to Git: 

git add logs/system_logs.txt 
git commit -m "Add system logs file for anomaly POC" 
git push 

 

 

 

5️⃣ Python AI Script 

File: ai/anomaly_detector.py 

Key points: 

import pandas as pd 
from sklearn.ensemble import IsolationForest 
 
# Path to logs inside container 
LOG_FILE = "logs/system_logs.txt" 
 
# Read logs 
with open(LOG_FILE, "r") as file: 
   logs = file.readlines() 
 
# Parse logs 
data = [] 
for log in logs: 
   parts = log.strip().split(" ", 3) 
   if len(parts) < 4: continue 
   timestamp = parts[0] + " " + parts[1] 
   level = parts[2] 
   message = parts[3] 
   data.append([timestamp, level, message]) 
 
df = pd.DataFrame(data, columns=["timestamp", "level", "message"]) 
df["timestamp"] = pd.to_datetime(df["timestamp"]) 
 
# Map log levels to numeric 
level_mapping = {"INFO":1, "WARNING":2, "ERROR":3, "CRITICAL":4} 
df["level_score"] = df["level"].map(level_mapping) 
df["message_length"] = df["message"].apply(len) 
 
# Isolation Forest for anomaly detection 
model = IsolationForest(contamination=0.1, random_state=42) 
df["anomaly"] = model.fit_predict(df[["level_score","message_length"]]) 
df["status"] = df["anomaly"].apply(lambda x: "❌ Anomaly" if x==-1 else "✅ Normal") 
 
# Print anomalies 
print("\n🔍 AI-Driven Log Anomaly Detection Results:\n") 
print(df) 
print("\n🚨 Detected Anomalies:\n", df[df["status"]=="❌ Anomaly"]) 
 

Important: Ensure log path matches container (logs/system_logs.txt) 

 

6️⃣ Docker Setup 

6.1 Dockerfile 

File: devops/Dockerfile 

FROM python:3.10-slim 
WORKDIR /app 
 
# Copy Python requirements 
COPY ai/requirements.txt . 
 
# Install dependencies 
RUN pip install --no-cache-dir -r requirements.txt 
 
# Copy source code and logs 
COPY ai/ ai/ 
COPY logs/ logs/ 
 
# Run anomaly detector 
CMD ["python", "ai/anomaly_detector.py"] 
 

6.2 Build Docker Image (Minikube) 

eval $(minikube docker-env) # Point Docker to Minikube 
docker build -t afs/ai-anomaly-detector -f devops/Dockerfile . 
docker images | grep afs/ai-anomaly-detector 
 

 

7️⃣ Kubernetes Setup 

7.1 CronJob YAML 

File: devops/cronjob.yaml 

apiVersion: batch/v1 
kind: CronJob 
metadata: 
 name: ai-log-anomaly-detector 
spec: 
 schedule: "*/5 * * * *" # Run every 5 minutes 
 jobTemplate: 
   spec: 
     template: 
       spec: 
         containers: 
         - name: anomaly-detector 
           image: afs/ai-anomaly-detector:latest 
           imagePullPolicy: IfNotPresent 
         restartPolicy: OnFailure 
 

7.2 Apply CronJob 

kubectl apply -f devops/cronjob.yaml 
kubectl get cronjob 
 

 

8️⃣ Run Manual Job (Testing) 

kubectl delete pods --all 
kubectl delete jobs --all 
kubectl create job --from=cronjob/ai-log-anomaly-detector ai-log-anomaly-detector-manual 
kubectl get pods 
kubectl logs <pod-name> 
 

✅ You should see normal and anomaly logs printed: 

✅ Normal 
❌ Anomaly 
 

 

9️⃣ Troubleshooting 

9.1 Common issues 

Issue 

Cause 

Solution 

FileNotFoundError: ../logs/system_logs.txt 

Wrong log path inside container 

Update LOG_FILE = "logs/system_logs.txt" in Python script 

ErrImagePull 

Kubernetes cannot find local Docker image 

Run eval $(minikube docker-env) before building image 

CrashLoopBackOff 

Script crashes (e.g., missing file) 

Check Python logs and fix path or dependencies 

No pods appear 

Job/CronJob not applied 

Use kubectl apply -f devops/cronjob.yaml and verify with kubectl get pods 

 

🔟 How the POC Works 

Docker container has Python code + logs 

CronJob runs periodically → launches a Kubernetes Job 

Job executes Python anomaly detection script 

Python reads logs, calculates numeric scores, message length, uses Isolation Forest 

Anomalies are printed in logs (❌ Anomaly) 

Can be extended to: 

Push alerts to Slack/email 

Store results in database or dashboard 

Monitor real-time cluster logs 

 

1️⃣1️⃣ Git Commands 

Track changes: 

git add . 
git commit -m "Add anomaly detection script and Docker setup" 
git push 
 

Useful for open-source contributions or CI/CD pipelines. 

 

1️⃣2️⃣ Extending the POC 

Monitor Kubernetes pod logs: mount /var/log/pods as volume 

CI/CD pipeline integration: run anomaly detector post-deployment 

Grafana dashboard: visualize anomalies over time 

Slack/Teams notifications: proactive alerting 

 

1️⃣3️⃣ Key Learnings 

Integration of AI models for predictive insights 

Containerized AI applications using Docker 

Automating periodic jobs with Kubernetes CronJobs 

Practical DevOps skills: 

Minikube setup 

Job & pod management 

Debugging CrashLoopBackOff & ErrImagePull 

 

✅ Conclusion 

This POC demonstrates: 

AI can automatically detect unusual log patterns 

DevOps teams can use it for predictive monitoring 

Fully containerized + Kubernetes-integrated for scalable deployment 

Flexible: works with any log type (application, system, DB, Kubernetes) 

Provides anomaly insights for better decision-making 

 
