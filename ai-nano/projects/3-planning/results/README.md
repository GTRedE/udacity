
_Udacity Artificial Intelligence Nanodegree, July 2017_
# Project 3: Implement a Planning Search
The **goal** of this project is to build a planning search agent that finds the optimal shipping routes for an air cargo transport system. 

The project includes basic skeletons for the classes and functions needed, but students must complete the missing pieces described below.

---
## Part 1: Planning Problems

#### 1. Implement methods and functions in `my_air_cargo_problems.py`

* `AirCargoProblem.get_actions` method including `load_actions` and `unload_actions` sub-functions

_Create concrete Action objects based on the domain action schema for: Load, Unload, and Fly. A concrete action is a specific literal action that does not include variables as with the schema. For example, the action schema `Load(c, p, a)` can represent the concrete actions `Load(C1, P1, SFO)` or `Load(C2, P2, JFK)`. The actions for the planning problem must be concrete because the problems in forward search and planning graphs must use propositional logic._

**Solution:** The source code for my solution can be found [here](). Below is a snippet showing the implementation of the Load action.

```python
def load_actions():
            """Create all concrete Load actions and return a list

            :return: list of Action objects
            """
            loads = []
            for a in self.airports:
                for p in self.planes:
                    for c in self.cargos:
                        # preconditions - make sure cargo and plane are At airport
                        precond_pos = [
                            expr("At({}, {})".format(c, a)),
                            expr("At({}, {})".format(p, a)),
                        ]
                        precond_neg = []
                        # positive action - put cargo In plane
                        effect_add = [expr("In({}, {})".format(c, p))]
                        # negative action - remove cargo At airport
                        effect_rem = [expr("At({}, {})".format(c, a))]
                        load = Action(expr("Load({}, {}, {})".format(c, p, a)),
                                        [precond_pos, precond_neg],
                                        [effect_add, effect_rem])
                        loads.append(load)
            return loads
```

* `AirCargoProblem.actions` method [(link to my code)]()

* `AirCargoProblem.result` method [(link to my code)]()

* `air_cargo_p2` function [(link to my code)]()

* `air_cargo_p3` function ([link to my code]() and snippet below)

```python
def air_cargo_p3():
    ''' Problem 3 Definition:
    Init(At(C1, SFO) ∧ At(C2, JFK) ∧ At(C3, ATL) ∧ At(C4, ORD)
    	∧ At(P1, SFO) ∧ At(P2, JFK)
    	∧ Cargo(C1) ∧ Cargo(C2) ∧ Cargo(C3) ∧ Cargo(C4)
    	∧ Plane(P1) ∧ Plane(P2)
    	∧ Airport(JFK) ∧ Airport(SFO) ∧ Airport(ATL) ∧ Airport(ORD))
    Goal(At(C1, JFK) ∧ At(C3, JFK) ∧ At(C2, SFO) ∧ At(C4, SFO))
    '''

    cargos = ['C1', 'C2', 'C3', 'C4']
    planes = ['P1', 'P2']
    airports = ['ATL', 'JFK', 'ORD', 'SFO']
    pos = [
            expr('At(C1, SFO)'),
            expr('At(C2, JFK)'),
            expr('At(C3, ATL)'),
            expr('At(C4, ORD)'),
            expr('At(P1, SFO)'),
            expr('At(P2, JFK)'),
           ]
    neg = [
            expr('At(C1, ATL)'),
            expr('At(C1, JFK)'),
            expr('At(C1, ORD)'),
            expr('At(C2, ATL)'),
            expr('At(C2, ORD)'),
            expr('At(C2, SFO)'),
            expr('At(C3, JFK)'),
            expr('At(C3, ORD)'),
            expr('At(C3, SFO)'),
            expr('At(C4, ATL)'),
            expr('At(C4, JFK)'),
            expr('At(C4, SFO)'),
            expr('At(P1, ATL)'),
            expr('At(P1, JFK)'),
            expr('At(P1, ORD)'),
            expr('At(P2, ATL)'),
            expr('At(P2, ORD)'),
            expr('At(P2, SFO)'),
            expr('In(C1, P1)'),
            expr('In(C1, P2)'),
            expr('In(C2, P1)'),
            expr('In(C2, P2)'),
            expr('In(C3, P1)'),
            expr('In(C3, P2)'),
            expr('In(C4, P1)'),
            expr('In(C4, P2)'),
           ]
    init = FluentState(pos, neg)
    goal = [
            expr('At(C1, JFK)'),
            expr('At(C2, SFO)'),
            expr('At(C3, JFK)'),
            expr('At(C4, SFO)'),
            ]
    return AirCargoProblem(cargos, planes, airports, init, goal)

```
 

---
## Part 2: Domain-Independent Heuristics

#### 2. Implement heuristic method in `my_air_cargo_problems.py`

* `AirCargoProblem.h_ignore_preconditions` method

#### 3. Implement a Planning Graph with automatic heuristics in `my_planning_graph.py`

* `PlanningGraph.add_action_level` method
* `PlanningGraph.add_literal_level` method
* `PlanningGraph.inconsistent_effects_mutex` method
* `PlanningGraph.interference_mutex` method
* `PlanningGraph.competing_needs_mutex` method
* `PlanningGraph.negation_mutex` method
* `PlanningGraph.inconsistent_support_mutex` method
* `PlanningGraph.h_levelsum` method


---
## Part 3: Written Analysis
* _Provide an optimal plan for Problems 1, 2, and 3.
* Compare and contrast non-heuristic search result metrics (optimality, time elapsed, number of node expansions) for Problems 1,2, and 3. Include breadth-first, depth-first, and at least one other uninformed non-heuristic search in your comparison; Your third choice of non-heuristic search may be skipped for Problem 3 if it takes longer than 10 minutes to run, but a note in this case should be included.
* Compare and contrast heuristic search result metrics using A* with the "ignore preconditions" and "level-sum" heuristics for Problems 1, 2, and 3.
* What was the best heuristic used in these problems? Was it better than non-heuristic search planning methods for all problems? Why or why not?
* Provide tables or other visual aids as needed for clarity in your discussion._


![problem 1](problem-1.jpg)


![problem 2](problem-2.jpg)


![problem 3](problem-3.jpg)




---
## Part 4: Research Review
### Instructions
The field of Artificial lIntelligence is continually changing and advancing. To be an AI Engineer at the cutting edge of your field, you need to be able to read and communicate some of these advancements with your peers. In order to help you get comfortable with this, in the second part of this project you will read a seminal paper in the field of Game-Playing and write a simple one page summary on it.

Write a simple one page summary covering the paper's goals, the techniques introduced, and results (if any).

### My Research Review
[Here is a link](https://github.com/tommytracey/udacity/tree/master/ai-nano/projects/2-isolation/results/research_review.pdf) to a PDF version of my research review on AlphaGo. The paper is titled, [Mastering the Game of Go with Deep Neural Networks and Tree Search](https://storage.googleapis.com/deepmind-media/alphago/AlphaGoNaturePaper.pdf), written by the team at Deep Mind and featured in the journal [Nature](https://www.nature.com/nature/journal/v529/n7587/full/nature16961.html) in January, 2016.

---
