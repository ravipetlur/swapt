import boto3
import logging

def elastic_ips_cleanup(region):
    client = boto3.client('ec2', region_name=region)
    addresses_dict = client.describe_addresses()
    for eip_dict in addresses_dict['Addresses']:
        if "InstanceId" not in eip_dict:
            print(eip_dict['PublicIp'] +
                  " doesn't have any instances associated, releasing")
            client.release_address(AllocationId=eip_dict['AllocationId'])


regions = [r['RegionName'] for r in boto3.client('ec2').describe_regions()['Regions']]

for region in regions:
    logging.info(f"Cleaning {region}")
    elastic_ips_cleanup(region)