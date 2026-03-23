from langgraph.graph import StateGraph
from typing import TypedDict

from nodes import skill_node, domain_node, question_node, evaluation_node



class State(TypedDict):
    text: str
    skills: str
    domain: str
    questions: str
    answer: str
    evaluation: str


def app_graph():
    graph = StateGraph(State)

    graph.add_node("skills", skill_node)
    graph.add_node("domain", domain_node)
    graph.add_node("questions", question_node)
    graph.add_node("evaluation", evaluation_node)

    graph.set_entry_point("skills")

    graph.add_edge("skills", "domain")
    graph.add_edge("domain", "questions")
    graph.add_edge("questions", "evaluation")

    compiled_graph = graph.compile()
    return compiled_graph

