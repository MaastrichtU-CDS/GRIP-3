import difflib

from vantage6.algorithm.tools.decorators import data
import pandas

MIN = 10
@data(1)
def calcIncidentie(data, target, period, *args, **kwargs):
    #Subtask
    #Collect all rows where target attribute has a specific value
    #And where the start and end attribute fall within a specific range
    #Data is a pandas dataframe

    #Only return an anwser when the count > MIN due to the risk of reidentification if only a few records are found
    count = len(data[(data[target['attribute']] == target['value']) & (data[period['start']['attribute']] >= period['start']['value']) & (data[period['end']['attribute']] < period['end']['value'])])
    return count if count > MIN else 0


@data(1)
def calc_local_Incidentie(data, target, start, *args, **kwargs):
    #Subtask
    #Collect all rows where target attribute has a specific value
    #And where the start falls on or after a certain date
    #E.g. how many individuals have code U71 starting at date 2022-2-2

    data[start['attribute']] = pandas.to_datetime(data[start['attribute']], errors='coerce')
    count = len(data[(data[target['attribute']] == target['value']) & (data[start['attribute']] >= start['value'])])
    return count