# Process-Discovery using Alpha-Miner Technique

## Introduction 

This program utilizes the -miner technique to extract process models from event logs. Its foundation was the notion of directly-follows relationships between activities in the log, with the goal of identifying the process' control-flow structure. Based on the order of occurrence in the log, I iteratively created a footprint table to illustrate the links between various actions. The simultaneous operations were then identified using a variety of rules, and the process model was built using sets of locations and flow interactions. 

In this implementation, I read and worked with event log data contained in a CSV file using the “pandas” library (imported as pd). For preprocessing and interacting with the event log data, it offered effective data manipulation, filtering, and analysis tools. 

I also created and examined a directed graph that reflected the found process model using the “networkx" library (imported as nx). I was able to build nodes and edges with this library and carry out a variety of graph-related tasks, which made it possible to analyze the process model. 

## Preprocessing the event log to generate multi-set of traces L and displaying it 

In this implementation, I read and worked with event log data contained in a CSV file using the pandas library (imported as pd). For preprocessing and interacting with the event log data, it offered effective data manipulation, filtering, and analysis tools. 

I also created and examined a directed graph that reflected the found process model using the networkx library (imported as nx). I was able to build nodes and edges with this library and carry out a variety of graph-related tasks, which made it possible to analyse the process model. 

The trace ID was added to a new empty list if it wasn't already there in the traces dictionary. The activity was then added to the list of activities linked to the relevant trace ID. I displayed the multiple-set of traces, designated as L, after iterating through all rows. I printed each trace's ID and the associated list of actions. This stage was crucial in getting the event log data ready for additional investigation and the identification of process models.

## Identifying and displaying set TL, start & end events (TI and TO) 

I took a series of traces and extract distinct status values, start events, and end events. In order to do this, I iterated through all the traces while initializing an empty set called TL. I used the update() method to add the distinct status values from each trace to the TL set during each cycle. I then iterated over the traces again using an empty set I constructed and called TI. I included the start event—the first event for each trace—to the TI set. Similar to that, I made an empty set called TO and went through the traces once more. This time, I added the end event—the final event—from each trace to the TO set. Finally, I printed the start events from the TI set, the end events from the TO set, and the unique status values from the TL set.

## Generating Footprint Table and Relationship Sets 

I created a footprint table to record the connections between the various activities in a collection of traces. To do this, I first initialized an empty data frame called footprint table and created a sorted list of distinct status values, TL. The cells in the table were then updated based on the connections between activities after I iterated over the traces. The symbols "->" and "-" denoted a direct succession, "-" a reverse succession, and "||" parallel activities. By looking for "->" linkages in both directions between pairs of activities in TL, I was also able to spot parallel activities. The footprint table was then saved as a CSV file. I created XL using the footprint table by considering activity pairs that had non-empty relationships in the table. In the end, I made YL by choosing couples from XL that had no other supersets. To analyze and carry out process mining duties, XL and YL both contributed useful information.

## Identifying and displaying set PL and FL 

Based on the YL set, I produced and printed the sets PL (Places) and FL (Flow Relations). I iterated over each pair (A, B) in YL to construct PL, adding frozensets of A and B to PL as I went. Additionally, I added the frozensets 'iL' and 'oL' to represent the start and end locations, respectively. I repeated each pair (A, B) in YL for FL. I made tuples within each pair to represent the connections between activities and locations. For each activity 'a' in A, I inserted a tuple with the activity as the first element and the corresponding frozenset from YL as the second element. Similar to this, I added a tuple with "b" as the second element for each action "b" in B, and the frozenset from YL as the first element. I also created tuples ('iL', t) and (t, 'oL') for each activity ('t') to explain the flow from the start and finish locations to the activities. I transformed the elements of PL and FL after producing them into a legible manner. I converted frozensets into strings in readable_PL by changing 'iL' and 'oL' to "Start" and "End," respectively, and sorting and connecting the activities included within the frozensets with commas. Similar to this, I changed frozensets in readable_FL into strings by replacing "iL" and "oL" with "Start" and "End," respectively, and sorting and connecting the activities included within the frozensets with commas. The sets PL (Places) and FL (Flow Relations) were then printed. I represented the components in readable_FL as the flow relations between activities or places and the elements in readable_PL as the places.
