from vantage6.common import info
from vantage6.algorithm.tools.decorators import algorithm_client

@algorithm_client
def grip3IncidentieTest(client, nodes, target, start, *args, **kwargs):
        #Main function
        #Simply iterates over all nodes and calls the subfunction
        info('Initializing nodes')
        count = 0;
        for node in nodes:
            count+= (_calc_local_incidence(client, [node], target, start))

        return count

def _calc_local_incidence(client, organizations,target, start):
    #Call the subtask
    task = client.task.create(
        name="grip_3",
        input_={'method': 'calc_local_Incidentie',
                "kwargs": {'target':target,'start': start} },
        organizations=organizations
    )
    return client.wait_for_results(task['id'])[0]

def _calc_local(client, organizations,target, period):
    #Call the subtask
    task = client.task.create(
        name="grip_3",
        input_={'method': 'calcIncidentie',
                "kwargs": {'target':target,'period': period} },
        organizations=organizations
    )
    return client.wait_for_results(task['id'])[0]
