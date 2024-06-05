# purpose: automatically start stopped servers in the morning 
#          and stop running servers at the end of the work day with times 
#          defined by tags named autostart and autostop
#
# TODO
#  - handle using 12 hour clock instead of expected 24 hour clock format
#  - other

import boto3
from datetime import datetime, timezone
import re

def validate_time_format(time_str):
    # Check if the time_str matches the HHMM format
    if re.match(r'^\d{4}$', time_str):
        hour = int(time_str[:2])
        minute = int(time_str[2:])
        return 0 <= hour < 24 and 0 <= minute < 60
    return False

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag-key', 
                'Values': ['autostart', 'autostop']
            }
        ]
    )

    start_instances = []
    stop_instances = []
    current_time = datetime.now(timezone.utc).strftime('%H%M')

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_state = instance['State']['Name']
            autostart = None
            autostop = None
            for tag in instance['Tags']:
                if tag['Key'] == 'autostart':
                    autostart = tag['Value']
                elif tag['Key'] == 'autostop':
                    autostop = tag['Value']
            
            # Validate the autostart and autostop formats
            if autostart and not validate_time_format(autostart):
                print(f'Invalid autostart format for instance {instance_id}: {autostart}')
                continue
            if autostop and not validate_time_format(autostop):
                print(f'Invalid autostop format for instance {instance_id}: {autostop}')
                continue
            
            # Determine if the current time is within the autostart and autostop range
            if autostart and autostop:
                if autostart <= current_time < autostop and instance_state == 'stopped':
                    start_instances.append(instance_id)
                elif (current_time < autostart or current_time >= autostop) and instance_state == 'running':
                    stop_instances.append(instance_id)

    if start_instances:
        ec2.start_instances(InstanceIds=start_instances)
        print('Started instances: ' + str(start_instances))
    else:
        print('No instances to start')

    if stop_instances:
        ec2.stop_instances(InstanceIds=stop_instances)
        print('Stopped instances: ' + str(stop_instances))
    else:
        print('No instances to stop')
