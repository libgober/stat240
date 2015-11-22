#test sending an email in python

import pandas as pd
import numpy as np
import os
#load the units
all_lawyers = pd.read_csv("California_Criminal_Lawyers.csv")
#exclude obviously bad units
lawyers_with_email = all_lawyers[all_lawyers.Email.notnull()]
#get rid of District Attorneys and Public Defenders
drop_list = ["district","public","pub def","US Attorney"]
public_agents = [any([i in x.lower() for i in drop_list]) for x in lawyers_with_email['Address']]
private_attorneys = [not x for x in public_agents]
population = lawyers_with_email[private_attorneys]
#randomly shuffle their order
np.random.seed(02143)
shuffled = population.reindex(np.random.permutation(population.index))
#assign to a treatment option
factor_level = [(i,j,k) for i in ["Black","White"] for j in ["Male","Female"] for k in ["40,000","80,000"]]
shuffled['race'] = [factor_level[i % 8][0]  for i in range(len(shuffled))]
shuffled['gender'] = [factor_level[i % 8][1]  for i in range(len(shuffled))]
shuffled['income'] = [factor_level[i % 8][2]  for i in range(len(shuffled))]
shuffled['assigned_order'] = [i for i in range(len(shuffled))]
#save the result
shuffled.to_csv("Pilot_Assignments.csv")
