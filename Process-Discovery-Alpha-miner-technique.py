import pandas as pd
import networkx as nx

# Read the event log CSV file into a pandas DataFrame
df = pd.read_csv('AnonymizedEventData.csv')

# Preprocessing the Event Log
traces = {}
for _, row in df.iterrows():
    trace_id = row['GroupName']
    activity = row['Status']
    if trace_id not in traces:
        traces[trace_id] = []
    traces[trace_id].append(activity)

# Displaying the Multi-set of Traces, L
print("Multi-set of Traces, L:")
for trace_id, trace in traces.items():
    print(f"Trace ID: {trace_id}")
    print(trace)
    print()

# Identifying unique Status values from the entire set L (TL)
TL = set()
for trace in traces.values():
    TL.update(trace)

# Identifying Start Events (TI)
TI = set()
for trace in traces.values():
    start_event = trace[0]
    TI.add(start_event)

# Identifying End Events (TO)
TO = set()
for trace in traces.values():
    end_event = trace[-1]
    TO.add(end_event)

# Displaying TL
print("\nTL (Unique Status from the entire set L):")
for status in TL:
    print(f"Status: {status}")

# Displaying TI
print("\nTI (Start Events):")
for event in TI:
    print(event)

# Displaying TO
print("\nTO (End Events):")
for event in TO:
    print(event)

# Generating the Footprint Table
TL = sorted(TL)
footprint_table = pd.DataFrame(index=TL, columns=TL)
footprint_table = footprint_table.fillna('#')

for trace in traces.values():
    for i in range(len(trace) - 1):
        current_activity = trace[i]
        next_activity = trace[i + 1]
        if footprint_table.loc[current_activity, next_activity] == '<-':
            footprint_table.loc[current_activity, next_activity] = '||'
        else:
            footprint_table.loc[current_activity, next_activity] = '->'

        # Update the reverse successors (<-)
        if footprint_table.loc[next_activity, current_activity] == '->':
            footprint_table.loc[next_activity, current_activity] = '||'
        elif footprint_table.loc[next_activity, current_activity] == '#':
            footprint_table.loc[next_activity, current_activity] = '<-'

for activity in TL:
    footprint_table.loc[activity, activity] = '#'

# Checking for parallel activities (||)
for i in range(len(TL)):
    for j in range(i + 1, len(TL)):
        activity1 = TL[i]
        activity2 = TL[j]
        if (footprint_table.loc[activity1, activity2] == '->' and
                footprint_table.loc[activity2, activity1] == '->'):
            footprint_table.loc[activity1, activity2] = '||'
            footprint_table.loc[activity2, activity1] = '||'

# Save the Footprint Table to a CSV file
footprint_table.to_csv('footprint_table.csv', index=True)

# Generating XL
XL = set()
for A in TL:
    for B in TL:
        if A and B and footprint_table.loc[A, B] != '#':
            XL.add((frozenset(A), frozenset(B)))

# Generating YL
YL = set()
for (A, B) in XL:
    flag = True
    for (A_prime, B_prime) in XL:
        if A_prime.issuperset(A) and B_prime.issuperset(B) and (A, B) != (A_prime, B_prime):
            flag = False
            break
    if flag:
        YL.add((A, B))

# Generating PL
PL = set()
for (A, B) in YL:
    PL.add(frozenset([frozenset(A), frozenset(B)]))
PL.add(frozenset(['iL']))
PL.add(frozenset(['oL']))

# Generating FL
FL = set()
for (A, B) in YL:
    for a in A:
        FL.add((a, frozenset([frozenset(A), frozenset(B)])))
    for b in B:
        FL.add((frozenset([frozenset(A), frozenset(B)]), b))
for t in TL:
    FL.add(('iL', t))
    FL.add((t, 'oL'))

# Convert PL elements to readable format
readable_PL = []
for place in PL:
    if place == frozenset(['iL']):
        readable_PL.append('Start')
    elif place == frozenset(['oL']):
        readable_PL.append('End')
    else:
        activities = ', '.join(sorted(str(activity) for activity in place))
        readable_PL.append(f'({activities})')

# Convert FL elements to readable format
readable_FL = []
for (a, b) in FL:
    if a == 'iL':
        readable_FL.append(('Start', b))
    elif b == 'oL':
        readable_FL.append((a, 'End'))
    else:
        activities = ', '.join(sorted(str(activity) for activity in b))
        for activity in b:
            readable_FL.append((a, activity))

# Print PL
print("\nPL (Places):")
for place in readable_PL:
    print(place.replace("frozenset(", "").replace(")", ""))

# Print FL (Flow Relations)
print("\nFL (Flow Relations):")
for arc in readable_FL:
    arc_str = ' '.join(str(a) for a in arc)
    arc_str = arc_str.replace("frozenset(", "").replace(")", "")
    print(arc_str)

# Printing Resultant Process
print("\nResultant Process")
for arc in readable_FL:
    arc_str = ' '.join(str(a) for a in arc)
    arc_str = arc_str.replace("frozenset(", "").replace(")", "")
    print(arc_str)

# Create a directed graph for the discovered process
G = nx.DiGraph()
G.add_nodes_from(readable_PL)
G.add_edges_from(readable_FL)

# Determine the fitness of each trace
fitness_scores = []
for trace in traces.values():
    current_place = 'Start'
    fitness_score = 0
    for activity in trace:
        next_place = None
        for successor in G.successors(current_place):
            if successor.startswith('Start ->'):
                continue
            if activity in successor:
                next_place = successor
                break
        if next_place:
            current_place = next_place
            fitness_score += 1
    fitness_scores.append(fitness_score / len(trace))

# Print the fitness scores for each trace
print("\nFitness Scores:")
for i, score in enumerate(fitness_scores):
    trace_id = list(traces.keys())[i]
    print(f"Trace ID: {trace_id} - Fitness Score: {score}")
