import pm4py
import log_sampling
import log_representativeness
import pandas as pd

logs_names = ["sepsis"]
ratios = [0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
column_names = ["log", "sample_ratio", "completeness", "coverage", "fitness", "precision", "F1"]
df = pd.DataFrame(columns=column_names)

k = 1

for name in logs_names:
    log = pm4py.read_xes("logs/" + name + ".xes")
    
    training, testing = log_sampling.seperate_test_training(log, 0.8)
    
    for ratio in ratios:

        print(f"---- RUN {k}/12 ----")
        k+=1
        
        sample = log_sampling.sample_log(training, ratio)
        net, im, fm = pm4py.discover_petri_net_inductive(sample)
        fitness = pm4py.fitness_alignments(testing, net, im, fm)['averageFitness']
        precision = pm4py.precision_alignments(testing, net, im, fm)
        F1 = (2*fitness*precision)/(fitness+precision)

        data = {
            "log": name,
            "sample_ratio": ratio,
            "completeness": log_representativeness.completeness_DF(sample),
            "fitness": fitness,
            "precision": precision,
            "F1": F1,
        }

        df.loc[len(df)] = data
        
    df.to_csv("output/out_" + name + "_inductive" + ".csv", index=False, header=True)


