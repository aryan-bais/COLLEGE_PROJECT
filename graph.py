from langgraph.graph import StateGraph
from typing import TypedDict
from nodes import interview_node


class State(TypedDict):
    text: str
    answer: str
    company: str
    result: str


def app_graph():
    graph = StateGraph(State)

    graph.add_node("interview", interview_node)

    graph.set_entry_point("interview")

    return graph.compile()