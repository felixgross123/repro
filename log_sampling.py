import pm4py
import math
import random

def log_to_listOfTraces_converter(log):
    traces = list()
    variants = pm4py.get_variants(log)
    for variant in variants:
        for i in range(variants[variant]):
            traces.append(variant)

    return traces

def lostOfTraces_to_log_converter(traces):
    string_traces = list()
    for trace in traces:
        traceString = ""
        for activity in trace:
            traceString += activity
            traceString += ","
        string_traces.append(traceString[:-1])
        
    return pm4py.parse_event_log_string(string_traces)

def seperate_test_training(log, training_ratio):

    traces = log_to_listOfTraces_converter(log)
    training_size = math.ceil(len(traces) * training_ratio)
    training_log = list()

    for i in range(training_size):
        r = random.randint(0, len(traces)-1)
        training_log.append(traces[r])
        del traces[r]

    testing_log = list(traces)

    return lostOfTraces_to_log_converter(training_log), lostOfTraces_to_log_converter(testing_log)


def sample_log(log, ratio):
    
    traces = log_to_listOfTraces_converter(log)
    sample_size = math.ceil(len(traces) * ratio)
    sample_log = list()

    for i in range(sample_size):
        r = random.randint(0, len(traces)-1)
        sample_log.append(traces[r])
        del traces[r]

    return lostOfTraces_to_log_converter(sample_log)