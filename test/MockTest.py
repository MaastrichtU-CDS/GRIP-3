from vantage6.algorithm.tools.mock_client import MockAlgorithmClient
from pathlib import Path

# get path of current directory
current_path = Path(__file__).parent

## Mock client
client = MockAlgorithmClient(
    datasets=[
        # Data for first organization
        [{
            "database": current_path / "demo_combined_data_node1.csv",
            "db_type": "csv",
            "input_data": {}
        }],
        # Data for second organization
        [{
            "database": current_path / "demo_combined_data_node2.csv",
            "db_type": "csv",
            "input_data": {}
        }],
        # Data for the third organisation
        [{
            "database": current_path / "demo_combined_data_node3.csv",
            "db_type": "csv",
            "input_data": {}
        }]
    ],
    # package name where main method is present
    module="com.grip3.vantage6wrapper"
)

# list mock organizations
organizations = client.organization.list()
org_ids = [organization["id"] for organization in organizations]

# 1. Wat is de incidentie van apendicities (D88=D88) en cholelithiasis (D98 / D98*)?
#   - incidentie:=episodes nieuw gestart in 2022
central_task = client.task.create(
    input_={'method': 'grip3Incidentie',
            'args': [org_ids, {'attribute': 'episode_icpc', 'value': 'D88'},
                     {'attribute': 'episode_datum_start', 'value': '2022-01-01'}]},
    organizations=[org_ids[0]],
)
results = client.wait_for_results(central_task.get("id"))

# Expected anwser: 0
print('- incidentie D88 per 1000 patient jaren: ' + str(results))

central_task = client.task.create(
    input_={'method': 'grip3Incidentie',
            'args': [org_ids, {'attribute': 'episode_icpc', 'value': 'D98'},
                     {'attribute': 'episode_datum_start', 'value': '2022-01-01'}]},
    organizations=[org_ids[0]],
)
results = client.wait_for_results(central_task.get("id"))

# Expected anwser 0.02
print('- incidentie D98 per 1000 patient jaren: ' + str(results))

# Vraag 2: Wat is de incidentie en prevalencie van OMA (H71) otitis... EN UWI (U71*)?')
# incidentie := episodes nieuw gestart in 2022')
# puntprevalentie op 31-12-2022 := patienten met 8 weken ervoor t/m 31-12-2022 een nieuwe episode H71 of U71 (aanname: duur  8 weken)')

central_task = client.task.create(
    input_={'method': 'grip3Incidentie',
            'args': [org_ids, {'attribute': 'episode_icpc', 'value': 'H71'},
                     {'attribute': 'episode_datum_start', 'value': '2022-01-01'}]},
    organizations=[org_ids[0]],
)
results = client.wait_for_results(central_task.get("id"))

# Expected anwser 0.15
print('- incidentie H71 per 1000 patient jaren: ' + str(results))

# Puntincidentie
central_task = client.task.create(
    input_={'method': 'grip3PuntIncidentie', 'args': [org_ids, {'attribute': 'episode_icpc', 'value': 'H71'},
                                                       {'attribute': 'episode_datum_start', 'value': '2022-10-01'},
                                                       {'attribute': 'episode_datum_start', 'value': '2022-12-31'}]},
    organizations=[org_ids[0]],
)
results = client.wait_for_results(central_task.get("id"))

# Expected anwser 0.07
print('-puntincidentie H71 per 1000 patient jaren: ' + str(results))

# Vraag 3: Wat is de gemiddelde BMI van mensen met DM2 (T90 of T90.02)
central_task = client.task.create(
    input_={'method': 'grip3AverageBMI', 'args': [org_ids, [{'attribute': 'episode_icpc', 'value': 'T90'},
                                                       {'attribute': 'episode_icpc', 'value': 'T90.02'}]]},
    organizations=[org_ids[0]],
)
results = client.wait_for_results(central_task.get("id"))

# Expected anwser 23
print('Average BMI: ' + str(results))