from vantage6.algorithm.tools.mock_client import MockAlgorithmClient
from pathlib import Path

# get path of current directory
current_path = Path(__file__).parent

## Mock client
client = MockAlgorithmClient(
    datasets=[
        # Data for first organization
        [{
            "database": current_path / "demo_combined_data_node3.csv",
            "db_type": "csv",
            "input_data": {}
        }]
    ],
    #package name where main method is present
    module="com.grip3.vantage6wrapper"
)

# list mock organizations
organizations = client.organization.list()
org_ids = [organization["id"] for organization in organizations]

# Run the central method on 1 node and get the results
central_task = client.task.create(
    input_={'method': 'grip3IncidentieTest',
            'args': [org_ids, {'attribute': 'episode_icpc', 'value': 'U71'}, {'attribute': 'episode_datum_start', 'value': '2000-12-31'}]},
    organizations=[org_ids[0]],
)
results = client.wait_for_results(central_task.get("id"))

## Expected output: 18
print(results)
