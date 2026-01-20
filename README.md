# afs-anamoly-poc
# AI-Driven Anomaly Detection – DevOps PoC

## Overview
This PoC demonstrates how AI-based anomaly detection can be integrated into DevOps log monitoring workflows to provide predictive insights and early detection of abnormal system behavior.

## Architecture
Logs → Feature Engineering → AI Model → Anomaly Detection → Alerts

## Tools Used
- Python
- Pandas
- Scikit-Learn
- Docker
- Kubernetes (CronJob)
- Isolation Forest (Unsupervised ML)

## DevOps Responsibilities
- Containerization of AI model
- Integration with log sources
- Scheduling via Kubernetes
- Automation and scalability

## AI Responsibilities
- Model selection
- Feature engineering
- Anomaly detection logic

## Use Cases
- Kubernetes pod failures
- Application error spikes
- Rare critical incidents
- Predictive incident detection (AIOps)

## How to Run Locally
```bash
pip install -r ai/requirements.txt
./run_local.sh
