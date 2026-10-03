import boto3
from datetime import datetime, timedelta, timezone

# =========================================================
# CONFIGURATION
# =========================================================

INSTANCE_ID = "i-07cdc1f01f242a366"
REGION = "ap-south-1"

# Demo/example rate only
EC2_HOURLY_RATE = 1.00

# Potential period for stopping the instance
POTENTIAL_STOPPED_HOURS = 10

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


# =========================================================
# GET EC2 INFORMATION
# =========================================================

response = ec2.describe_instances(
    InstanceIds=[INSTANCE_ID]
)

instance = response["Reservations"][0]["Instances"][0]

state = instance["State"]["Name"]
instance_type = instance["InstanceType"]
launch_time = instance["LaunchTime"]


# =========================================================
# RUNNING DURATION
# =========================================================

current_time = datetime.now(timezone.utc)

running_duration = current_time - launch_time

running_hours = (
    running_duration.total_seconds() / 3600
)


# =========================================================
# ESTIMATED CURRENT COST
# =========================================================

estimated_cost = (
    running_hours * EC2_HOURLY_RATE
)


# =========================================================
# POTENTIAL SAVINGS
# =========================================================

potential_savings = (
    POTENTIAL_STOPPED_HOURS * EC2_HOURLY_RATE
)


# =========================================================
# GET CPU UTILIZATION
# =========================================================

end_time = datetime.now(timezone.utc)

start_time = (
    end_time - timedelta(hours=1)
)

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
# REPORT
# =========================================================

print()
print("EC2 COST OPTIMIZATION REPORT")
print("============================")

print("Instance ID:", INSTANCE_ID)
print("Instance Type:", instance_type)
print("Current State:", state)

print()
print("INSTANCE INFORMATION")
print("--------------------")

print("Launch Time:", launch_time)

print(
    "Running Duration:",
    running_duration
)

print(
    "Running Hours:",
    round(running_hours, 2)
)

print(
    "Estimated Cost: ₹",
    round(estimated_cost, 2)
)


# =========================================================
# CPU REPORT
# =========================================================

print()
print("CPU ANALYSIS")
print("------------")

if average_cpu is not None:

    print(
        "Average CPU:",
        round(average_cpu, 2),
        "%"
    )

    print(
        "CPU Data Points:",
        len(datapoints)
    )

else:

    print("CPU data is not available yet.")


# =========================================================
# POTENTIAL SAVINGS
# =========================================================

print()
print("POTENTIAL SAVINGS")
print("-----------------")

print(
    "Potential Stop Time:",
    POTENTIAL_STOPPED_HOURS,
    "hours"
)

print(
    "Potential Compute Savings: ₹",
    round(potential_savings, 2)
)


# =========================================================
# RECOMMENDATION
# =========================================================

print()
print("COST OPTIMIZATION RECOMMENDATION")
print("---------------------------------")

if state == "running" and average_cpu is not None:

    if average_cpu < CPU_THRESHOLD:

        print(
            "Finding: EC2 appears potentially underutilized."
        )

        print(
            "Action: Review whether the instance can be"
        )

        print(
            "stopped or downsized during low-usage periods."
        )

        print(
            "Potential Compute Saving: ₹",
            round(potential_savings, 2)
        )

    else:

        print(
            "Finding: CPU utilization does not indicate"
        )

        print(
            "obvious underutilization."
        )

        print(
            "Action: Continue monitoring usage."
        )

elif state == "stopped":

    print(
        "EC2 is currently stopped."
    )

    print(
        "Compute charges are not incurred while stopped,"
    )

    print(
        "but storage and other applicable charges may remain."
    )

else:

    print(
        "Not enough information for a recommendation."
    )