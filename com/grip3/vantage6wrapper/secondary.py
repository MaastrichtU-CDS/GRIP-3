from vantage6.algorithm.tools.decorators import data

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

