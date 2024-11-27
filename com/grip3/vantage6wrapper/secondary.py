import difflib

from vantage6.algorithm.tools.decorators import data
import pandas

MIN = 10


@data(1)
def calcIncidentie(data, target, period, *args, **kwargs):
    # Subtask
    # Collect all rows where target attribute has a specific value
    # And where the start and end attribute fall within a specific range
    # Data is a pandas dataframe

    # Only return an anwser when the count > MIN due to the risk of reidentification if only a few records are found
    count = len(data[(data[target['attribute']] == target['value']) & (
                data[period['start']['attribute']] >= period['start']['value']) & (
                                 data[period['end']['attribute']] < period['end']['value'])])
    return count if count > MIN else 0


@data(1)
def calc_local_Incidentie(data, target, start, *args, **kwargs):
    # Subtask
    # Collect all rows where target attribute has a specific value
    # And where the start falls on or after a certain date
    # E.g. how many individuals have code U71 starting at date 2022-2-2

    data[start['attribute']] = pandas.to_datetime(data[start['attribute']], errors='coerce')
    count = len(data[(data[target['attribute']].str.startswith(target['value'], na=False)) & (
                data[start['attribute']] >= start['value'])])

    population = int(data['populatie'][0])
    res = {"count": count, "population": population}
    return res


@data(1)
def calc_local_punt_Incidentie(data, target, start, end, *args, **kwargs):
    # Subtask for point incidence,
    data[start['attribute']] = pandas.to_datetime(data[start['attribute']], errors='coerce')
    count = len(data[(data[target['attribute']].str.startswith(target['value'], na=False)) & (
                data[start['attribute']] >= start['value']) & (data[end['attribute']] < end['value'])])

    population = int(data['populatie'][0])
    res = {"count": count, "population": population}
    return res

@data(1)
def calc_local_average_bmi(data, requirements, *args, **kwargs):

    # Select IDs that have the correct disease requirements
    requirements_ids = pandas.DataFrame(columns=data.columns)
    for attribute in requirements:
        requirements_ids = pandas.concat([requirements_ids, data[data[attribute['attribute']] == attribute['value']]])

    requirements_ids= requirements_ids.drop_duplicates('pat_studie_id')

    data = data[data['pat_studie_id'].isin(requirements_ids['pat_studie_id'])]

    #Select length
    length = data[data['uitslag_bepaling_nr'] == 560]
    #Select latest measurements
    length = length.sort_values('uitslag_datum', ascending=False).drop_duplicates('pat_studie_id')[
        ['pat_studie_id', 'uitslag_waarde_numeriek']]
    length['length'] = length['uitslag_waarde_numeriek']
    length.drop(columns='uitslag_waarde_numeriek')
    #Select weight
    weight = data[data['uitslag_bepaling_nr'] == 357]
    #Select latest measurements
    weight = weight.sort_values('uitslag_datum', ascending=False).drop_duplicates('pat_studie_id')[
        ['pat_studie_id', 'uitslag_waarde_numeriek']]

    weight['weight'] = weight['uitslag_waarde_numeriek']
    weight.drop(columns='uitslag_waarde_numeriek')

    # Merge into 1 dataset
    patients = pandas.merge(length, weight, on="pat_studie_id", how='inner')

    #Calc BMI
    patients['BMI'] = patients['weight'] / (patients['length'] * patients['length'])
    average = patients['BMI'].mean()
    population = patients.shape[0]
    return {'average': average, 'population': population}
