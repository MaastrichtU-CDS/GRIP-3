from vantage6.common import info
from vantage6.algorithm.tools.decorators import algorithm_client

@algorithm_client
def grip3Test(client, nodes, target, period, *args, **kwargs):
        #Main function
        #Simply iterates over all nodes and calls the subfunction
        info('Initializing nodes')
        count = 0;
        for node in nodes:
            count+= (_calc_local(client, [node], target, period))

        return count

def _calc_local(client, organizations,target, period):
    #Call the subtask
    task = client.task.create(
        name="grip_3",
        input_={'method': 'calcIncidentie',
                "kwargs": {'target':target,'period': period} },
        organizations=organizations
    )
    return client.wait_for_results(task['id'])[0]
