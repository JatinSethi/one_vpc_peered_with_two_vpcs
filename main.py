import boto3
from cli_parser import parser

client  = None
ec2     = None

'''
|   This method is responsible for iniating the resources required to communicate with AWS usng boto3
'''
def initiate_originators(access_key_id=None, secret_access_key=None, region=None):
    global client
    global ec2
    # if any one of the required paramters are missing, assume that default credentials and rconfig file is there
    # default credentials and configs are either there in the ~/.aws/ or set as environment variables
    if None in [access_key_id, secret_access_key, region]:
        client  = boto3.client('ec2')
        ec2     = boto3.resource('ec2')
    else:
        client = boto3.client(
            'ec2',
            aws_access_key_id = access_key_id,
            aws_secret_access_key = secret_access_key,
            region_name = region
        )
        ec2 = boto3.resource(
            'ec2',
            aws_access_key_id = access_key_id,
            aws_secret_access_key = secret_access_key,
            region_name = region
        )

'''
|   Provisions a VPC
'''
def create_vpc(cidr_block, dry_run=False):
    response = client.create_vpc(
        CidrBlock=cidr_block, 
        DryRun=dry_run
    )
    return ec2.Vpc(response['Vpc']['VpcId'])

'''
|   Provisions a VPC Peering Connection between two VPCs
'''
def create_peering_between(vpc_requestor, vpc_acceptor):
    return vpc_requestor.request_vpc_peering_connection(
        PeerVpcId=vpc_acceptor.vpc_id
    )

'''
|   Adds an entry into the routes table
'''
def create_route_between(vpc0, vpc1, peering_connection):
    route_table = None

    # pick the first route table
    for table in vpc0.route_tables.all():
        route_table = table
        break;

    # add an entry into the route table
    return route_table.create_route(
        DestinationCidrBlock=vpc1.cidr_block,
        VpcPeeringConnectionId=peering_connection.vpc_peering_connection_id
    )

def main():

    # collect all the arguments
    args = parser.parse_args()

    # create aws requestors
    initiate_originators(args.key_id, args.access_key, args.region_name)

    # for naming and printing only
    main_vpc_name       = 'vpc-0(main)'
    client1_vpc_name    = 'vpc-1(customer-1)'
    client2_vpc_name    = 'vpc-2(customer-2)'

    # CidrBlocks from command line
    cidr_A = args.vpc0
    cidr_B = args.vpc1
    cidr_C = args.vpc2

    print("%s: %s" %(main_vpc_name, cidr_A))
    print("%s: %s" %(client1_vpc_name, cidr_B))
    print("%s: %s" %(client2_vpc_name, cidr_C))

    try:
        '''
        | VPC Provisioning
        '''
        print("\nProvisioning %s" %(main_vpc_name))
        vpc_A = create_vpc(cidr_A)
        print('%s ID: %s' %(main_vpc_name, vpc_A.vpc_id));

        print("\nProvisioning %s" %(client1_vpc_name))
        vpc_B = create_vpc(cidr_B)
        print('%s ID: %s' %(client1_vpc_name, vpc_B.vpc_id));

        print("\nProvisioning %s" %(client2_vpc_name))
        vpc_C = create_vpc(cidr_C)
        print('%s ID: %s' %(client2_vpc_name, vpc_C.vpc_id));

        print()

        '''
        | Subnet Provisioning
        '''
        print("\nProvisioning Subnet for %s" %(main_vpc_name))
        subnet_A = vpc_A.create_subnet(
            CidrBlock=vpc_A.cidr_block,
        )
        print('%s Subnet ID: %s' %(main_vpc_name, subnet_A.subnet_id))

        print("\nProvisioning Subnet for %s" %(client1_vpc_name))
        subnet_B = vpc_B.create_subnet(
            CidrBlock=vpc_B.cidr_block,
        )
        print('%s Subnet ID: %s' %(client1_vpc_name, subnet_B.subnet_id))

        print("\nProvisioning Subnet for %s" %(client2_vpc_name))
        subnet_C = vpc_C.create_subnet(
            CidrBlock=vpc_C.cidr_block,
        )
        print('%s Subnet ID: %s' %(client2_vpc_name, subnet_C.subnet_id))

        print()

        '''
        | VPC Peering Connection Provisioning
        '''
        print('\nProvisioning VPC Peering connection between %s and %s' % (main_vpc_name, client1_vpc_name))
        peering_connection_AB = create_peering_between(vpc_A, vpc_B)

        # accept the vpc peering connection
        print('Accepting VPC peering connection (ID: %s)' %(peering_connection_AB.vpc_peering_connection_id))
        peering_connection_AB.accept()

        print()

        print('\nProvisioning VPC Peering connection between %s and %s' % (main_vpc_name, client2_vpc_name))
        peering_connection_AC = create_peering_between(vpc_A, vpc_C)

        # accept the vpc peering connection
        print('Accepting VPC peering connection (ID: %s)' %(peering_connection_AC.vpc_peering_connection_id))
        peering_connection_AC.accept()

        print()

        '''
        | Routes provisioning
        '''
        print('Establishing routes between %s and %s' %(main_vpc_name, client1_vpc_name))
        route_A = create_route_between(vpc_A, vpc_B, peering_connection_AB)
        route_B = create_route_between(vpc_B, vpc_A, peering_connection_AB)

        # add entries into the routing table of vpc-B
        print('Establishing routes between %s and %s' %(main_vpc_name, client2_vpc_name))
        route_A = create_route_between(vpc_A, vpc_C, peering_connection_AC)
        route_C = create_route_between(vpc_C, vpc_A, peering_connection_AC)

    except Exception as e:
        print("Error Occurred")
        print(e)

if __name__ == '__main__':
  main()