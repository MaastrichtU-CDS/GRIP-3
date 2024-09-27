from vantage6.algorithm.tools.mock_client import MockAlgorithmClient
from pathlib import Path

# get path of current directory
current_path = Path(__file__).parent

## Mock client
client = MockAlgorithmClient(
    datasets=[
        # Data for first organization
        [{
            "database": current_path / "df_grip3_test_node_1.csv",
            "db_type": "csv",
            "input_data": {}
        }],
        # Data for second organization
        [{
            "database": current_path / "df_grip3_test_node_2.csv",
            "db_type": "csv",
            "input_data": {}
        }],
        # Data for the third organisation
        [{
            "database": current_path / "df_grip3_test_node_3.csv",
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
    input_={'method': 'grip3Test',
            'args': [org_ids, {'attribute': 'age', 'value': 60}, {'start': {'attribute': 'start', 'value': 2023},
                                            'end': {'attribute': 'end', 'value': 2025}}]},
    organizations=[org_ids[0]],
)
results = client.wait_for_results(central_task.get("id"))

## Expected output: 28
## Dataset 1 & 2 both contain 14 examples, dataset 3 contains 2 examples, which is below the allowed threshold
print(results)
