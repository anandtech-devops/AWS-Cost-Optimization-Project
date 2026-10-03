# AWS Cost Optimization Project

A practical AWS cost optimization and resource analysis project built using **Terraform, Python, Boto3, Amazon EC2, Amazon CloudWatch, Amazon EBS, and AWS Cost Explorer**.

The project analyzes AWS infrastructure and billing information to identify **potential cost optimization opportunities** without automatically modifying or deleting production resources.

---

## Project Objective

The goal of this project is to build a simple automation workflow that can:

* Provision AWS infrastructure using Terraform
* Retrieve EC2 resource information using Boto3
* Analyze EC2 CPU utilization using CloudWatch
* Identify potentially unused EBS volumes
* Retrieve AWS billing data using Cost Explorer
* Generate a consolidated cost optimization report
* Run the analysis automatically using Windows Task Scheduler

---

## Project Flow

```text
Terraform
    |
    v
AWS EC2
    |
    +------------------+
    |                  |
    v                  v
CloudWatch           EBS
CPU Metrics      Volume Analysis
    |                  |
    +--------+---------+
             |
             v
        Python / Boto3
             |
      +------+------+
      |             |
      v             v
   EC2 API    Cost Explorer
      |             |
      +------+------+
             |
             v
   Cost Optimization Report
             |
             v
   Windows Task Scheduler
```

---

## Technologies Used

| Technology                 | Purpose                                  |
| -------------------------- | ---------------------------------------- |
| **Terraform**              | AWS infrastructure provisioning          |
| **AWS EC2**                | Compute resource used for the lab        |
| **Amazon CloudWatch**      | EC2 CPU metric analysis                  |
| **Amazon EBS**             | Storage resource analysis                |
| **AWS Cost Explorer**      | AWS billing information                  |
| **Python**                 | Automation and report generation         |
| **Boto3**                  | AWS API integration                      |
| **AWS CLI**                | AWS resource verification and management |
| **Windows Task Scheduler** | Scheduled report execution               |
| **Git & GitHub**           | Source control and project documentation |

---

## Project Structure

```text
AWS-Cost-Optimization-Project/
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
├── .gitignore
└── .terraform.lock.hcl
```

> Terraform state files and the `.terraform/` directory are intentionally excluded from the repository.

---

# 1. Infrastructure Provisioning with Terraform

Terraform is used to provision the EC2 lab instance.

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

AWS provider configuration:

```hcl
provider "aws" {
  region = "ap-south-1"
}
```

The project uses the AWS Mumbai region for the lab infrastructure.

---

# 2. EC2 Resource Analysis

Python and Boto3 are used to retrieve EC2 information such as:

* Instance ID
* Instance type
* Current instance state

The script then combines this information with CloudWatch CPU metrics.

The current CPU analysis threshold is:

```text
10%
```

If the analyzed CPU utilization is below this threshold, the application reports:

```text
EC2 appears potentially underutilized.
```

The project **does not automatically stop, terminate, or resize the EC2 instance**.

The result is treated as a finding that requires further review.

---

# 3. CloudWatch CPU Analysis

The project retrieves the EC2:

```text
AWS/EC2
CPUUtilization
```

metric from Amazon CloudWatch.

Current analysis configuration:

```text
Analysis window : Last 1 hour
Metric period   : 5 minutes
Statistic       : Average
```

Example lab result:

```text
Average CPU : 0.15%
Data Points : 12
```

Because this is a learning project with a short monitoring history, this result is treated only as a **potential underutilization finding**.

For a real production environment, longer historical data would be required before making right-sizing or scheduling decisions.

---

# 4. EBS Analysis

The project uses the EC2 API to inspect EBS volumes.

The analyzer checks:

```text
Volume size
Volume type
Volume state
```

A volume with:

```text
State = available
```

is identified as a **potentially unused EBS volume**, because it is not currently attached to an EC2 instance.

A test EBS volume was created during development to validate this detection logic.

The analyzer successfully detected the test volume as:

```text
1 potentially unused EBS volume(s) detected.
```

The project **does not automatically delete EBS volumes**.

---

# 5. AWS Cost Explorer

AWS Cost Explorer is used to retrieve billing information through the AWS API.

The Python application uses the Cost Explorer service endpoint:

```python
cost_explorer = boto3.client(
    "ce",
    region_name="us-east-1"
)
```

The infrastructure itself is deployed in:

```text
ap-south-1
```

The Cost Explorer API is accessed through its supported service endpoint while the resources being analyzed remain in the Mumbai region.

The project retrieves:

```text
UnblendedCost
```

for the selected billing period.

---

# 6. Consolidated Cost Optimization Report

The main script:

```text
cost_report.py
```

combines information from multiple AWS services.

```text
EC2 Information
       +
CloudWatch CPU Metrics
       +
EBS Analysis
       +
Cost Explorer Billing
       |
       v
Consolidated Cost Optimization Report
```

Example report structure:

```text
=======================================================
           AWS COST OPTIMIZATION REPORT
=======================================================

RESOURCE INFORMATION
-------------------------------------------------------
Region        : ap-south-1
Instance ID   : <EC2 instance ID>
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
Total Storage : <current storage>
Unused Volumes: <current count>
Finding       : Potential unused volume(s) detected.

AWS BILLING
-------------------------------------------------------
Billing Period: <selected period>
AWS Cost      : <Cost Explorer value>

OPTIMIZATION SUMMARY
-------------------------------------------------------
[1] CPU: Potential utilization finding
[2] EBS: Potential unused volume finding
[3] Billing: Cost Explorer data retrieved
```

The report is designed to provide **evidence for review rather than automatically performing destructive actions**.

---

# 7. Automation

Windows Task Scheduler is used to execute:

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

The scheduled task was successfully tested.

Verification returned:

```text
LastTaskResult : 0
```

which indicates that the scheduled task completed successfully.

---

# 8. Safety Approach

The project follows a:

```text
Detect → Analyze → Report → Review
```

approach.

The application:

* Does not automatically terminate EC2 instances
* Does not automatically delete EBS volumes
* Does not automatically resize resources
* Does not claim guaranteed cost savings
* Reports potential optimization opportunities for human review

This approach reduces the risk of accidentally modifying AWS resources during analysis.

---

# 9. Key Learning Outcomes

Through this project, I practiced:

* Terraform infrastructure provisioning
* AWS EC2 management
* CloudWatch metric retrieval
* EBS resource analysis
* AWS Cost Explorer API
* Python automation
* Boto3 AWS SDK
* AWS CLI
* AWS cost optimization concepts
* Scheduled automation
* Git and GitHub workflow
* Basic AWS API integration

---

# 10. Future Improvements

Possible future improvements include:

* Longer-term CPU utilization analysis
* Daily and weekly automated reports
* Cost reports grouped by AWS service
* SNS/email notifications
* GitHub Actions automation
* Additional CloudWatch metrics
* Automated resource tagging checks
* Right-sizing analysis
* Dashboard visualization

---

## Disclaimer

This is a **learning and portfolio project**.

The optimization findings are recommendations for review and are not automatic production decisions.

AWS billing can vary depending on factors such as region, usage, operating system, pricing model, credits, refunds, and billing adjustments.

The project should therefore be treated as a demonstration of **AWS monitoring, API-based analysis, Terraform provisioning, Python automation, and cost optimization concepts** rather than as a complete production FinOps platform.
