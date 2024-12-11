import vantage6.client as v6client
from vantage6.client import UserClient as Client


def setup(config):
    """
    This function authenticates a client.

    It creates a client with the given configuration details, authenticates the client,
    and sets up encryption for the client.

    Parameters:
    config (object): An object containing configuration details.
    It should have the following attributes:
        - server_url: The server URL.
        - server_port: The server port.
        - server_api: The server API.
        - username: The username for authentication.
        - password: The password for authentication.
        - organization_key: The private key of the user's organisation to set up end-to-end encryption.

    Returns:
        Client: An authenticated client with encryption set up.
    """
    # Create a client
    client = Client(config.get('server_url'), config.get('server_port'), config.get('server_api'),
                    log_level='debug')
    # Authenticate the client
    client.authenticate(config.get('username'), config.get('password'))

    # Set up encryption for the client
    if config.get('organization_key') == '':
        config['organization_key'] = None
    client.setup_encryption(config.get('organization_key'))

    return client


# Config for demo enviroment that can be created using v6 dev create-demo-network
json = {
    "collaboration": 1,
    "aggregating_organisation": 1,
    "server_url": "http://localhost",
    "server_port": 7601,
    "server_api": "/api",
    "username": "dev_admin",
    "password": "password",
    "organization_key": ""
}

node1 = 2
node2 = 3
commodity_node = 2
exclude = [5, 6]
# Image name
IMAGE = 'fvandaalen/grip3:test'
NAME = 'grip3'
nodes = [node1, node2]

collaboration_id = 1

client = setup(json)

active_nodes = client.node.list(is_online=True)
active_nodes = active_nodes['data']
org_ids = [n['organization']['id'] for n in active_nodes]
print(f' Active nodes{org_ids}')

task = client.task.create(name=NAME, image=IMAGE, description=NAME,
                          collaboration=collaboration_id,
                          organizations=[commodity_node],
                          input_={'method': 'grip3Incidentie',
                                  'args': [nodes, {'attribute': 'episode_icpc', 'value': 'H71'},
                                           {'attribute': 'episode_datum_start', 'value': '2022-01-01'}]},
                          databases=[{'label': 'default'}]
                          )

done = False
i = 0

result = client.wait_for_results(task['id'])

print(result)
