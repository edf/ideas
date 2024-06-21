import argparse
import boto3
import requests

def get_instance_id():
    # Get the instance ID from the metadata service
    try:
        response = requests.get("http://169.254.169.254/latest/meta-data/instance-id")
        return response.text
    except requests.RequestException:
        print("Error retrieving instance ID from metadata service. Using default value.")
        return "i-1234567890abcdef0"  # Default instance ID (change as needed)

def describe_volumes(instance_id):
    # Initialize the EC2 client
    ec2 = boto3.client('ec2', region_name='us-east-2')

    # Describe volumes
    response = ec2.describe_volumes(
        Filters=[
            {
                'Name': 'attachment.instance-id',
                'Values': [instance_id]
            }
        ]
    )

    # Prepare data for printing
    data = []
    for volume in response['Volumes']:
        name = volume.get('Tags', [{'Value': 'N/A'}])[0]['Value']
        description = volume.get('Tags', [{'Value': 'N/A'}])[0]['Value']
        device = volume['Attachments'][0]['Device']
        device_type = volume['VolumeType']
        device_size = f"{volume['Size']} GB"
        iops = volume.get('Iops', 'N/A')
        throughput = volume.get('Throughput', 'N/A')
        data.append((name, description, device, device_type, device_size, iops, throughput, volume['VolumeId']))

    # Determine column widths based on the largest value in each column or header
    headers = ["Name", "Description", "Device", "Device Type", "Device Size", "IOPS", "Throughput", "VolumeID"]
    column_widths = [max(len(header), max(len(str(item)) for item in column)) for header, column in zip(headers, zip(*data))]

    # Print the output in a table format with headers
    print(" | ".join(f"{header:{width}}" for header, width in zip(headers, column_widths)))
    print("-" * sum(column_widths))
    for row in data:
        print(" | ".join(f"{item:{width}}" for item, width in zip(row, column_widths)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Describe EC2 volumes for a given instance ID")
    parser.add_argument("--instance-id", default=get_instance_id(), help="EC2 instance ID (default: metadata service)")

    args = parser.parse_args()
    describe_volumes(args.instance_id)
