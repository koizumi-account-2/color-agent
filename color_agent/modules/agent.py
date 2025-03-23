from langgraph.graph import StateGraph, END
from color_agent.modules.models import State
from color_agent.modules.nodes import PurposeGenerator, SuggestionColor, CheckSuggestion

class ColorAgent:
    def __init__(self, llm):
        self.purpose_gen = PurposeGenerator(llm)
        self.suggester = SuggestionColor(llm)
        self.checker = CheckSuggestion(llm)
        self.graph = self._create_graph()

    def _purpose_node(self, state: State) -> dict:
        print("purpose_node")
        purpose = self.purpose_gen.run(state.query)
        return {"purpose": purpose}

    def _suggestion_node(self, state: State) -> dict:
        print("suggestion_node")
        suggestion_list = self.suggester.run(state.purpose)
        return {"suggestions": suggestion_list.suggestions}

    def _check_node(self, state: State) -> dict:
        print("check_node")
        return self.checker.run(state)

    def _create_graph(self):
        builder = StateGraph(State)
        builder.add_node("purpose_node", self._purpose_node)
        builder.add_node("suggestion_node", self._suggestion_node)
        builder.add_node("check_node", self._check_node)

        builder.set_entry_point("purpose_node")
        builder.add_edge("purpose_node", "suggestion_node")
        builder.add_edge("suggestion_node", "check_node")
        builder.add_conditional_edges("check_node", lambda s: s.current_judge, {
            True: END,
            False: "purpose_node"
        })
        return builder.compile()

    def run(self, query: str) -> State:
        return self.graph.invoke(State(query=query))