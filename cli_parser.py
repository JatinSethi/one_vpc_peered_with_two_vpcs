import argparse

# initiate the parser
parser = argparse.ArgumentParser(
        description="Create and Setup VPC peerring connection where one central VPC is peered with two VPCs")

# add required argument for main VPC
parser.add_argument(
    'vpc0', 
    help="The central VPC's CidrBlock value in the format: IP/range, eg: 173.0.0.0/16"
)

# add required argument for client-1 VPC
parser.add_argument(
    'vpc1', 
    help="The Customer VPC's CidrBlock value in the format: IP/range, eg: 192.0.0.0/16"
)

# add required argument for client-2 VPC
parser.add_argument(
    'vpc2', 
    help="The Customer VPC's CidrBlock value in the format: IP/range, eg: 10.0.0.0/16"
)

# add optional argument for aws_access_key_id
parser.add_argument(
    '--key_id', 
    help="AWS aws_access_key_id to use. Provide this argument if you have not configured your local machine using AWS CLI"
)

# add optional argument for aws_secret_access_key
parser.add_argument(
    '--access_key', 
    help="AWS aws_secret_access_key to use. Provide this argument if you have not configured aws using AWS CLI"
)

# add optional argument for aws_secret_access_key
parser.add_argument(
    '--region_name', 
    help="AWS region to use. Provide this argument if you have not configured aws using AWS CLI"
)
