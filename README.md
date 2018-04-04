# One VPC Peered with Two VPCs (using Boto3)
This is a demonstration of automating the task of provisioning a 3 VPC peering layout where one central VPC is peered with two VPCs in an AWS environment. The communication is between only the main and a peer VPC, there is no communication between two peer VPCs. Refer to: [AWS VPC Peering Guide](https://docs.aws.amazon.com/AmazonVPC/latest/PeeringGuide/peering-configurations-full-access.html#one-to-two-vpcs-full-access), from this guide the demonstration was shaped.

## Pre-requisites:
- Python3 installed
- `pip` installed
- `aws_access_key_id` of your AWS account
- `aws_secret_access_key` of your AWS account
- `region` to use with your AWS account

## Steps to setup the Project:
- `git clone` this project or download zip and extract it
- cd into the project directory and run:

    `pip install -r requirements.txt`

## Usage:
    python poc.py [-h] [--key_id KEY_ID] [--access_key ACCESS_KEY]
                  [--region_name REGION_NAME]
                  vpc0 vpc1 vpc2

    Create and Setup VPC peerring connection where one central VPC is peered with two VPCs

    positional arguments:
      vpc0                  The central VPC's CidrBlock value in the format:
                            IP/range, eg: 173.0.0.0/16
      vpc1                  The Customer VPC's CidrBlock value in the format:
                            IP/range, eg: 192.0.0.0/16
      vpc2                  The Customer VPC's CidrBlock value in the format:
                            IP/range, eg: 10.0.0.0/16

    optional arguments:
      -h, --help            show this help message and exit
      --key_id KEY_ID       AWS aws_access_key_id to use. Provide this argument if
                            you have not configured your local machine using AWS
                            CLI
      --access_key ACCESS_KEY
                            AWS aws_secret_access_key to use. Provide this
                            argument if you have not configured aws using AWS CLI
      --region_name REGION_NAME
                            AWS region to use. Provide this argument if you have
                            not configured aws using AWS CLI
## Description:
### `vpc0`: 
Required. This is the main VPC that will be connected to the other two

### `vpc1`: 
Required. This is a vpc that will be connected to main vpc, `vpc0`, and not to any other.
This represents a client/customer

### `vpc2`: 
Required. This is a another vpc that will be connected to main vpc, `vpc0`, and not to any other.
This represents another client/customer

### `--key_id`, `--access_key`, `--region_name`:
Optional. If used, these paramters must be used together.
You should use these values when you have not configured AWS credentials on your machine. Or if you have configured your machine and want to override the default ones, then also you can use the arguments.
Read more about configuring AWS credentials on your local machine [here](https://boto3.readthedocs.io/en/latest/guide/configuration.html#interactive-configuration)

- `--key_id` is the value for `aws_access_key_id` in your AWS account.
- `--access_key` is the value for `aws_secret_access_key` in your AWS account.
- `--region_name` is the value for `region` in your AWS account.

### Pictorial representation

      (client-1)  (client-2)
          vpc1      vpc2
            \      /
              vpc0
             (main)
