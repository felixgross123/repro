import pm4py

def df(log):
    df_rels_w_freq = dict()
    variants = pm4py.get_variants(log)

    for variant in variants:
        df_rels_variant = set()
        for i in range(len(variant)-1):
            df_rels_variant.add((variant[i], variant[i+1]))

        for df_rel_variant in df_rels_variant:
            if df_rel_variant in df_rels_w_freq:
                df_rels_w_freq[df_rel_variant] += variants[variant]
            else:
                df_rels_w_freq[df_rel_variant] = variants[variant]

    return df_rels_w_freq

def chao2_DF_estimator(log):
    DF_relations_w_freq = df(log)
    DF_relations = list(DF_relations_w_freq.keys())

    no_singletons = 0
    no_doubletons = 0

    for DF_relation in DF_relations:
        if DF_relations_w_freq[DF_relation] == 1:
            no_singletons += 1
        elif DF_relations_w_freq[DF_relation] == 2:
            no_doubletons += 1
        
    if no_doubletons > 0:
        return len(DF_relations) + ((no_singletons ** 2)/(2 * no_doubletons))
    else:
        return len(DF_relations) + ((no_singletons * (no_singletons - 1))/2)

def completeness_DF(log):
    DF_relations = list(df(log).keys())
    return len(DF_relations)/chao2_DF_estimator(log)

def coverage_DF(log):
    DF_relations_w_freq = df(log)
    DF_relations = list(DF_relations_w_freq.keys())

    no_singletons = 0
    no_doubletons = 0
    no_total = 0

    for DF_relation in DF_relations:
        no_total += DF_relations_w_freq[DF_relation]
        if DF_relations_w_freq[DF_relation] == 1:
            no_singletons += 1
        elif DF_relations_w_freq[DF_relation] == 2:
            no_doubletons += 1
    
    no_traces = sum(trace for trace in pm4py.get_variants(log).values())

    if (no_singletons == 0 and no_doubletons == 0): return 1

    return 1 - (no_singletons / no_total) * (((no_traces - 1) * no_singletons)/((no_traces - 1) * no_singletons + 2 * no_doubletons))