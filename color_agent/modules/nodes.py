from color_agent.modules.models import Purpose, ColorSuggestionList, Judgement, State
from color_agent.modules.prompts import purpose_prompt, suggestion_prompt, check_prompt
import json

class PurposeGenerator:
    def __init__(self, llm):
        print("PurposeGenerator",Purpose)
        self.llm = llm.with_structured_output(Purpose)

    def run(self, query: str) -> Purpose:
        print("purpose_prompt",purpose_prompt)
        return (purpose_prompt | self.llm).invoke({"user_query": query})

class SuggestionColor:
    def __init__(self, llm):
        self.llm = llm.with_structured_output(ColorSuggestionList)

    def run(self, purpose: Purpose) -> ColorSuggestionList:
        print("suggestion_prompt")
        return (suggestion_prompt | self.llm).invoke(purpose.model_dump())

class CheckSuggestion:
    def __init__(self, llm):
        self.llm = llm.with_structured_output(Judgement)

    def run(self, state: State) -> dict:
        print("check_prompt",state.suggestions)
        suggestions = state.suggestions[-3:]
        suggestions_text = json.dumps([s.model_dump() for s in suggestions], ensure_ascii=False, indent=2)
        result = (check_prompt | self.llm).invoke({
            "query": state.query,
            "suggestions": suggestions_text
        })
        return {
            "current_judge": result.current_judge,
            "judge_reason": result.reason
        }