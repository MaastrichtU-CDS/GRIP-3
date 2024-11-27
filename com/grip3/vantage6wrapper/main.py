from vantage6.common import info
from vantage6.algorithm.tools.decorators import algorithm_client


@algorithm_client
def grip3AverageBMI(client, nodes, requirements, *args, **kwargs):
        #Main function
        #Simply iterates over all nodes and calls the subfunction
        info('Initializing nodes')
        averages = []
        for node in nodes:
            averages.append((_calc_local_bmi(client, [node], requirements)))

        bmi = 0
        pop = 0
        for average in averages:
            bmi += average["average"] * average["population"]
            pop += average["population"]
        return round(bmi / pop)

@algorithm_client
def grip3Incidentie(client, nodes, target, start, *args, **kwargs):
        #Main function
        #Simply iterates over all nodes and calls the subfunction
        info('Initializing nodes')
        incidenties = []
        for node in nodes:
            incidenties.append((_calc_local_incidence(client, [node], target, start)))

        count = 0
        pop = 0
        for inc in incidenties:
            count += inc["count"]
            pop += inc["population"]
        return round(count / pop * 1000 , 2)

@algorithm_client
def grip3PuntIncidentie(client, nodes, target, start,end, *args, **kwargs):
    # Main function
    # Simply iterates over all nodes and calls the subfunction
    info('Initializing nodes')
    incidenties = []
    for node in nodes:
        incidenties.append((_calc_local_punt_incidence(client, [node], target, start,end)))

    count = 0
    pop = 0
    for inc in incidenties:
        count += inc["count"]
        pop += inc["population"]
    return round(count / pop * 1000, 2)

def _calc_local_bmi(client, organizations, requirements):
    #Call the subtask
    task = client.task.create(
        name="grip_3",
        input_={'method': 'calc_local_average_bmi',
                "kwargs": {'requirements': requirements} },
        organizations=organizations
    )
    return client.wait_for_results(task['id'])[0]

def _calc_local_incidence(client, organizations,target, start):
    #Call the subtask
    task = client.task.create(
        name="grip_3",
        input_={'method': 'calc_local_Incidentie',
                "kwargs": {'target':target,'start': start} },
        organizations=organizations
    )
    return client.wait_for_results(task['id'])[0]

def _calc_local_punt_incidence(client, organizations,target, start,end):
    #Call the subtask
    task = client.task.create(
        name="grip_3",
        input_={'method': 'calc_local_punt_Incidentie',
                "kwargs": {'target':target,'start': start,'end':end} },
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
