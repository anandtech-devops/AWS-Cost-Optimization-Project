# AWS Cost Optimization Project

A practical AWS cost optimization and resource analysis project built using **Terraform, Python, Boto3, Amazon CloudWatch, Amazon EC2, Amazon EBS, and AWS Cost Explorer**.

The project identifies potential AWS cost optimization opportunities by analyzing EC2 utilization, EBS volumes, and AWS billing data.

---

## Project Objective

The main objective of this project is to build a simple automation tool that can:

* Provision AWS infrastructure using Terraform
* Monitor EC2 CPU utilization using CloudWatch
* Analyze EBS volumes and identify potentially unused volumes
* Retrieve AWS billing information using Cost Explorer
* Generate a consolidated cost optimization report
* Automatically execute the report using Windows Task Scheduler

---

## Architecture

```text
                    Terraform
                       |
                       v
                  AWS EC2 Instance
                       |
             +---------+---------+
             |                   |
             v                   v
        CloudWatch              EBS
        CPU Metrics          Volume Analysis
             |                   |
             +---------+---------+
                       |
                       v
                  Python / Boto3
                       |
             +---------+---------+
             |                   |
             v                   v
       EC2 API              Cost Explorer
             |                   |
             +---------+---------+
                       |
                       v
             Cost Optimization Report
                       |
                       v
              Windows Task Scheduler
                Automatic Execution
```

---

## Technologies Used

* **AWS**
* **Terraform**
* **Python**
* **Boto3**
* **Amazon EC2**
* **Amazon CloudWatch**
* **Amazon EBS**
* **AWS Cost Explorer**
* **AWS CLI**
* **Windows Task Scheduler**
* **Git & GitHub**

---

## Project Structure

```text
aws-cost-optimization-project/
│
├── provider.tf
├── main.tf
│
├── cost_report.py
├── cost_explorer.py
├── ec2_status.py
├── ebs_analyzer.py
│
├── README.md
└── .gitignore
```

---

## 1. Infrastructure Provisioning

Terraform is used to provision the EC2 instance.

Example:

```hcl
resource "aws_instance" "cost_lab" {
  ami           = "ami-0f918f7e67a3323f0"
  instance_type = "t3.micro"

  tags = {
    Name = "cost-optimization-lab"
  }
}
```

The Terraform provider is configured for the AWS Mumbai region:

```hcl
provider "aws" {
  region = "ap-south-1"
}
```

---

## 2. EC2 Cost Analysis

The Python script uses Boto3 to retrieve EC2 information such as:

* Instance ID
* Instance type
* Current state

CloudWatch CPU metrics are also retrieved for the EC2 instance.

The project currently uses a CPU threshold of:

```text
10%
```

If recent CPU utilization is below this threshold, the tool reports:

```text
EC2 appears potentially underutilized.
```

The tool does **not automatically stop or terminate the instance**.

It only provides a finding for further review.

---

## 3. CloudWatch CPU Analysis

The project retrieves EC2 `CPUUtilization` metrics from Amazon CloudWatch.

Current analysis window:

```text
Last 1 hour
```

Metrics are collected in:

```text
5-minute periods
```

Example result:

```text
Average CPU   : 0.15 %
Data Points   : 12
```

Because this is a learning project with a short monitoring history, the result is treated as a **potential underutilization finding**, not as a production scaling decision.

---

## 4. EBS Analysis

The Python application uses the EC2 API to inspect EBS volumes.

It checks:

```text
Volume size
Volume type
Volume state
```

A volume with:

```text
State = available
```

is treated as a potentially unused EBS volume because it is not attached to an EC2 instance.

Example test:

```text
Volume ID : vol-0541f96ed475d2dd4
Size      : 1 GB
Type      : gp3
State     : available
```

The analyzer successfully detected this test volume as:

```text
1 potentially unused EBS volume(s) detected.
```

The project does not automatically delete EBS volumes.

---

## 5. AWS Cost Explorer

AWS Cost Explorer is used to retrieve actual AWS billing data through the AWS API.

The Python application uses:

```python
cost_explorer = boto3.client(
    "ce",
    region_name="us-east-1"
)
```

The EC2 and CloudWatch resources are located in:

```text
ap-south-1
```

The Cost Explorer API is called using its supported endpoint.

The project retrieves `UnblendedCost` for the selected billing period.

---

## 6. Consolidated Cost Report

The main script:

```text
cost_report.py
```

combines:

```text
EC2 information
+
CloudWatch CPU metrics
+
EBS analysis
+
Cost Explorer billing data
```

and generates a single report.

Example:

```text
=======================================================
           AWS COST OPTIMIZATION REPORT
=======================================================

RESOURCE INFORMATION
-------------------------------------------------------
Region        : ap-south-1
Instance ID   : i-07cdc1f01f242a366
Instance Type : t3.micro
Current State : running

CPU ANALYSIS
-------------------------------------------------------
Average CPU   : 0.15 %
Data Points   : 12
Finding       : EC2 appears potentially underutilized.
Action        : Review usage before downsizing or stopping.

EBS ANALYSIS
-------------------------------------------------------
Total Storage : 48 GB
Unused Volumes: 0
Finding       : No unused EBS volumes detected.

AWS BILLING
-------------------------------------------------------
AWS Cost      : Cost Explorer value

OPTIMIZATION SUMMARY
-------------------------------------------------------
[1] CPU: Potential underutilization identified.
[2] EBS: No unused EBS volumes identified.
[3] Billing: Cost Explorer data successfully retrieved.
```

---

## 7. Automation

Windows Task Scheduler is used to automatically execute:

```text
cost_report.py
```

The automation flow is:

```text
Windows Task Scheduler
        |
        v
Python
        |
        v
cost_report.py
        |
        +---- EC2 API
        |
        +---- CloudWatch API
        |
        +---- EBS API
        |
        +---- Cost Explorer API
        |
        v
Cost Optimization Report
```

The scheduled task was successfully tested with:

```text
LastTaskResult : 0
```

---

## 8. Safety Approach

This project follows a **detect first, action later** approach.

The application:

* Does not automatically terminate EC2 instances
* Does not automatically delete EBS volumes
* Does not claim guaranteed cost savings
* Reports potential optimization opportunities for review

This prevents accidental deletion or interruption of AWS resources.

---

## 9. Key Learning Outcomes

Through this project, I practiced:

* Terraform infrastructure provisioning
* AWS EC2 management
* CloudWatch metric retrieval
* EBS resource analysis
* AWS Cost Explorer API
* Python automation
* Boto3 AWS SDK
* AWS CLI
* Cost optimization concepts
* Scheduled automation
* Git and GitHub workflow

---

## 10. Future Improvements

Possible future improvements include:

* Longer-term CPU utilization analysis
* Daily/weekly automated reports
* Cost reports grouped by AWS service
* SNS/email notifications
* GitHub Actions automation
* More detailed CloudWatch analysis
* Automated tagging checks
* Right-sizing recommendations
* Dashboard visualization

---

## Disclaimer

This is a learning and portfolio project.

The optimization findings are recommendations for review and are not automatic production decisions. AWS pricing and billing can vary based on region, operating system, usage, pricing model, credits, and other AWS billing factors.
