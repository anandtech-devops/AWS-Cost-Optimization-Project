import boto3
from datetime import datetime, timedelta, timezone


# =========================================================
# CONFIGURATION
# =========================================================

REGION = "ap-south-1"

INSTANCE_ID = "i-07cdc1f01f242a366"

# CPU threshold for underutilization
CPU_THRESHOLD = 10


# =========================================================
# AWS CLIENTS
# =========================================================

ec2 = boto3.client(
    "ec2",
    region_name=REGION
)

cloudwatch = boto3.client(
    "cloudwatch",
    region_name=REGION
)

cost_explorer = boto3.client(
    "ce",
    region_name="us-east-1"
)


# =========================================================
# GET EC2 INFORMATION
# =========================================================

response = ec2.describe_instances(
    InstanceIds=[INSTANCE_ID]
)

instance = response["Reservations"][0]["Instances"][0]

instance_type = instance["InstanceType"]
state = instance["State"]["Name"]


# =========================================================
# GET CPU UTILIZATION
# =========================================================

end_time = datetime.now(timezone.utc)

start_time = end_time - timedelta(hours=1)


cpu_response = cloudwatch.get_metric_statistics(
    Namespace="AWS/EC2",
    MetricName="CPUUtilization",
    Dimensions=[
        {
            "Name": "InstanceId",
            "Value": INSTANCE_ID
        }
    ],
    StartTime=start_time,
    EndTime=end_time,
    Period=300,
    Statistics=["Average"]
)

datapoints = cpu_response["Datapoints"]


# =========================================================
# CPU ANALYSIS
# =========================================================

if datapoints:

    cpu_values = [
        point["Average"]
        for point in datapoints
    ]

    average_cpu = (
        sum(cpu_values) / len(cpu_values)
    )

else:

    average_cpu = None


# =========================================================
# GET EBS INFORMATION
# =========================================================

ebs_response = ec2.describe_volumes()

volumes = ebs_response["Volumes"]

total_storage = 0
unused_volumes = 0


for volume in volumes:

    size = volume["Size"]
    volume_state = volume["State"]

    total_storage = (
        total_storage + size
    )

    if volume_state == "available":

        unused_volumes = (
            unused_volumes + 1
        )


# =========================================================
# GET AWS COST FROM COST EXPLORER
# =========================================================

today = datetime.now(timezone.utc).date()

cost_end_date = today

cost_start_date = today - timedelta(days=30)


cost_response = cost_explorer.get_cost_and_usage(
    TimePeriod={
        "Start": cost_start_date.strftime("%Y-%m-%d"),
        "End": cost_end_date.strftime("%Y-%m-%d")
    },
    Granularity="MONTHLY",
    Metrics=[
        "UnblendedCost"
    ]
)


# =========================================================
# COST ANALYSIS
# =========================================================

cost_results = cost_response["ResultsByTime"]

total_aws_cost = 0.0


for result in cost_results:

    amount = float(
        result["Total"]["UnblendedCost"]["Amount"]
    )

    total_aws_cost = (
        total_aws_cost + amount
    )


# =========================================================
# DETERMINE CPU FINDING
# =========================================================

if average_cpu is not None:

    if average_cpu < CPU_THRESHOLD:

        cpu_finding = (
            "EC2 appears potentially underutilized."
        )

        cpu_action = (
            "Review usage before downsizing or stopping."
        )

    else:

        cpu_finding = (
            "No obvious CPU underutilization detected."
        )

        cpu_action = (
            "Continue monitoring usage."
        )

else:

    cpu_finding = (
        "Not enough CPU data for analysis."
    )

    cpu_action = (
        "Collect more CloudWatch data."
    )


# =========================================================
# DETERMINE EBS FINDING
# =========================================================

if unused_volumes > 0:

    ebs_finding = (
        f"{unused_volumes} potentially unused EBS volume(s) detected."
    )

    ebs_action = (
        "Review volumes before deletion."
    )

else:

    ebs_finding = (
        "No unused EBS volumes detected."
    )

    ebs_action = (
        "No EBS cleanup finding."
    )


# =========================================================
# FINAL REPORT
# =========================================================

print()
print("=" * 55)
print("           AWS COST OPTIMIZATION REPORT")
print("=" * 55)


# =========================================================
# RESOURCE INFORMATION
# =========================================================

print()
print("RESOURCE INFORMATION")
print("-" * 55)

print("Region        :", REGION)
print("Instance ID   :", INSTANCE_ID)
print("Instance Type :", instance_type)
print("Current State :", state)


# =========================================================
# CPU ANALYSIS
# =========================================================

print()
print("CPU ANALYSIS")
print("-" * 55)

if average_cpu is not None:

    print(
        "Average CPU   :",
        round(average_cpu, 2),
        "%"
    )

    print(
        "Data Points   :",
        len(datapoints)
    )

else:

    print(
        "Average CPU   : Data not available"
    )


print(
    "Finding       :",
    cpu_finding
)

print(
    "Action        :",
    cpu_action
)


# =========================================================
# EBS ANALYSIS
# =========================================================

print()
print("EBS ANALYSIS")
print("-" * 55)

print(
    "Total Storage :",
    total_storage,
    "GB"
)

print(
    "Unused Volumes:",
    unused_volumes
)

print(
    "Finding       :",
    ebs_finding
)

print(
    "Action        :",
    ebs_action
)


# =========================================================
# AWS BILLING
# =========================================================

print()
print("AWS BILLING")
print("-" * 55)

print(
    "Billing Period:",
    cost_start_date,
    "to",
    cost_end_date
)

print(
    "AWS Cost      :",
    round(total_aws_cost, 8),
    "USD"
)


# =========================================================
# OPTIMIZATION SUMMARY
# =========================================================

print()
print("OPTIMIZATION SUMMARY")
print("-" * 55)

if average_cpu is not None and average_cpu < CPU_THRESHOLD:

    print(
        "[1] CPU:",
        "Potential underutilization identified."
    )

else:

    print(
        "[1] CPU:",
        "No obvious optimization finding."
    )


if unused_volumes > 0:

    print(
        "[2] EBS:",
        "Potential unused volume(s) identified."
    )

else:

    print(
        "[2] EBS:",
        "No unused EBS volumes identified."
    )


print(
    "[3] Billing:",
    "Cost Explorer data successfully retrieved."
)


# =========================================================
# FINAL STATUS
# =========================================================

print()
print("=" * 55)
print(
    "EC2 + CloudWatch + EBS + Cost Explorer analysis completed."
)
print("=" * 55)
print()
