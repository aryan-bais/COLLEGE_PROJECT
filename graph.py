from langgraph.graph import StateGraph
from nodes import skill_node, domain_node, question_node, evaluation_node


def app_graph():
    graph = StateGraph(dict)
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