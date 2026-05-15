# 🚀 Scalable Web App with ALB and Auto Scaling on AWS

## 📌 Project Overview
This project demonstrates a scalable web application deployment on AWS using Application Load Balancer (ALB) and Auto Scaling Group (ASG). The system automatically handles high traffic by distributing requests across multiple EC2 instances and scaling resources based on demand.

---

## 🧰 AWS Services Used
- Amazon EC2
- Application Load Balancer (ALB)
- Auto Scaling Group (ASG)
- Launch Template
- Target Group
- Security Groups
- AWS CLI
- Python Boto3

---

## ⚙️ Features
- Automatic scaling of EC2 instances
- Load balancing across servers
- High availability and fault tolerance
- Health checks for instances
- AWS infrastructure automation using Python

---

## 🚀 Steps to Run

```bash
python create_keypair.py
python create_security_group.py
python create_target_group.py
python create_alb.py
python create_listener.py
python create_launch_template.py
python create_autoscaling.py
