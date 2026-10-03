import boto3
from datetime import datetime, timedelta, timezone

# EC2 details
INSTANCE_ID = "i-07cdc1f01f242a366"
REGION = "ap-south-1"

# Connect to CloudWatch
cloudwatch = boto3.client(
    "cloudwatch",
    region_name=REGION
)

# Analyze last 7 days
end_time = datetime.now(timezone.utc)
start_time = end_time - timedelta(days=7)

# Get CPU utilization
response = cloudwatch.get_metric_statistics(
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
    Period=3600,
    Statistics=[
        "Average",
        "Minimum",
        "Maximum"
    ]
)

datapoints = response["Datapoints"]

# Check whether data exists
if not datapoints:
    print("No CPU data available yet.")

else:
    print("EC2 COST OPTIMIZATION REPORT")
    print("============================")
    print("Instance:", INSTANCE_ID)
    print("Analysis Period: Last 7 Days")
    print()

    # Sort data by time
    datapoints = sorted(
        datapoints,
        key=lambda x: x["Timestamp"]
    )

    print("CPU Data")
    print("--------")

    for point in datapoints:
        print(
            point["Timestamp"],
            "| Average:",
            round(point["Average"], 2),
            "%",
            "| Min:",
            round(point["Minimum"], 2),
            "%",
            "| Max:",
            round(point["Maximum"], 2),
            "%"
        )

    # Calculate overall average
    average_cpu = sum(
        point["Average"]
        for point in datapoints
    ) / len(datapoints)

    # Overall minimum and maximum
    minimum_cpu = min(
        point["Minimum"]
        for point in datapoints
    )

    maximum_cpu = max(
        point["Maximum"]
        for point in datapoints
    )

    print()
    print("SUMMARY")
    print("-------")
    print("Data points:", len(datapoints))
    print("Average CPU:", round(average_cpu, 2), "%")
    print("Minimum CPU:", round(minimum_cpu, 2), "%")
    print("Maximum CPU:", round(maximum_cpu, 2), "%")

    print()
    print("RECOMMENDATION")
    print("--------------")

    if average_cpu < 10:
        print(
            "EC2 appears to be potentially underutilized."
        )
        print(
            "Consider reviewing instance size or usage pattern."
        )

    else:
        print(
            "CPU utilization does not indicate obvious underutilization."
        )