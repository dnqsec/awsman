#!/usr/bin/env python
import sys
import os
import boto3
from botocore.exceptions import ClientError

instance_id = ''
action = ''
if len(sys.argv) == 2:
    action = sys.argv[1].upper()

ec2 = boto3.client('ec2')
ec2r = boto3.resource('ec2')



if action == 'START':
    # Do a dryrun first to verify permissions
    try:
        ec2.start_instances(InstanceIds=[instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, run start_instances without dryrun
    try:
        response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
        print("Started")
        instance_obj = ec2r.Instance(instance_id)
        dns_name = instance_obj.public_dns_name
        os.system('ssh -i "~/Aws.pem" ubuntu@'+ dns_name )
    except ClientError as e:
        print(e)

elif action == 'STATUS':
    instance_obj = ec2r.Instance(instance_id)
    dns_name = instance_obj.public_dns_name
    if dns_name == '':
        print('Instance down')
    else:
        print('Instance up')
elif action == 'CONNECT':
    instance_obj = ec2r.Instance(instance_id)
    dns_name = instance_obj.public_dns_name
    if dns_name != '':
        os.system('ssh -i "~/Aws.pem" ubuntu@'+ dns_name )
    else:
        print("Instance down")
elif action == 'STOP':
     # Do a dryrun first to verify permissions
    try:
        ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, call stop_instances without dryrun
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
        print("Stopped")
    except ClientError as e:
        print(e)

else:
    print('Usage: '+ sys.argv[0] +' start|stop|connect|status')   
