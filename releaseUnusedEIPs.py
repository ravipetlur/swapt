import boto3
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)


def elastic_ips_cleanup(region):
    client = boto3.client('ec2', region_name=region)
    addresses_dict = client.describe_addresses()
    for eip_dict in addresses_dict['Addresses']:
        if "InstanceId" not in eip_dict:
            logging.info("{eip_dict['PublicIp']} doesn't have any instances associated, releasing")
            client.release_address(AllocationId=eip_dict['AllocationId'])


regions = [r['RegionName'] for r in boto3.client('ec2').describe_regions()['Regions']]

for region in regions:
    logging.info("Cleaning {region}")
    elastic_ips_cleanup(region)