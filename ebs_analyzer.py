import boto3

# =========================================================
# CONFIGURATION
# =========================================================

REGION = "ap-south-1"

# Demo/example rate only
EBS_GB_MONTHLY_RATE = 10.0


# =========================================================
# AWS CLIENT
# =========================================================

ec2 = boto3.client(
    "ec2",
    region_name=REGION
)


# =========================================================
# GET EBS VOLUMES
# =========================================================

response = ec2.describe_volumes()

volumes = response["Volumes"]


print()
print("EBS COST ANALYSIS")
print("=================")


# =========================================================
# CHECK VOLUMES
# =========================================================

if not volumes:

    print("No EBS volumes found.")

else:

    total_storage = 0

    for volume in volumes:

        volume_id = volume["VolumeId"]
        size = volume["Size"]
        state = volume["State"]
        volume_type = volume["VolumeType"]

        # Add volume size to total
        total_storage = total_storage + size

        print()
        print("Volume ID:", volume_id)
        print("Size:", size, "GB")
        print("Type:", volume_type)
        print("State:", state)

        # Check whether volume is attached
        if volume["Attachments"]:

            instance_id = volume["Attachments"][0]["InstanceId"]

            print(
                "Attached To:",
                instance_id
            )

            print(
                "Finding: EBS volume is attached to an EC2 instance."
            )

            print(
                "Action: No unused-volume finding."
            )

        else:

            print(
                "Attached To: None"
            )

            print(
                "Finding: Potentially unused EBS volume."
            )

            print(
                "Action: Review before deletion."
            )


    # =====================================================
    # COST CALCULATION
    # =====================================================

    estimated_monthly_cost = (
        total_storage * EBS_GB_MONTHLY_RATE
    )


    print()
    print("EBS COST SUMMARY")
    print("================")

    print(
        "Total EBS Storage:",
        total_storage,
        "GB"
    )

    print(
        "Demo Rate: ₹",
        EBS_GB_MONTHLY_RATE,
        "per GB/month"
    )

    print(
        "Estimated Monthly Cost: ₹",
        round(estimated_monthly_cost, 2)
    )

    print()
    print(
        "Note: This is a demo estimate, not the actual AWS bill."
    )