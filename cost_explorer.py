import boto3
from datetime import datetime, timedelta


# =========================================================
# CONFIGURATION
# =========================================================

REGION = "us-east-1"


# =========================================================
# AWS CLIENT
# =========================================================

ce = boto3.client(
    "ce",
    region_name=REGION
)


# =========================================================
# DATE RANGE
# =========================================================

end_date = datetime.now().date()

start_date = end_date - timedelta(days=30)


# =========================================================
# GET AWS COST
# =========================================================

response = ce.get_cost_and_usage(
    TimePeriod={
        "Start": start_date.strftime("%Y-%m-%d"),
        "End": end_date.strftime("%Y-%m-%d")
    },
    Granularity="MONTHLY",
    Metrics=[
        "UnblendedCost"
    ]
)


# =========================================================
# DISPLAY COST
# =========================================================

print()
print("AWS COST EXPLORER REPORT")
print("========================")

for result in response["ResultsByTime"]:

    period = result["TimePeriod"]

    amount = result["Total"]["UnblendedCost"]["Amount"]

    unit = result["Total"]["UnblendedCost"]["Unit"]

    print()
    print(
        "Period:",
        period["Start"],
        "to",
        period["End"]
    )

    print(
        "Cost:",
        amount,
        unit
    )