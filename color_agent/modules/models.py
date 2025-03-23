from pydantic import BaseModel, Field
from typing import Annotated, Optional
import operator

class Purpose(BaseModel):
    tone: str = Field(...,description="雰囲気・感情")
    user_context: str = Field(...,description="UIの使用場面")
    target_user: str = Field(...,description="想定ユーザー層")
    emotion: str = Field(...,description="色の心理効果")

class ColorSuggestion(BaseModel):
    color: str = Field(...,description="色のコード")
    name: str = Field(...,description="色の名前")
    reason: str = Field(...,description="色選択の理由")

class ColorSuggestionList(BaseModel):
    suggestions:  Annotated[list[ColorSuggestion],operator.add] = Field(default_factory=list,description="提案履歴")

class State(BaseModel):
    query: str = Field(...,description="ユーザーの質問")
    purpose: Optional[Purpose] = Field(default=None, description="ユーザー要求の目的分析結果")
    current_role: str = Field(default="",description="選定された回答ロール")
    suggestions: ColorSuggestionList= Field(default=ColorSuggestionList(),description="提案履歴")
    current_judge: bool = Field(default=False,description="品質チェックの結果")
    judge_reason: str = Field(default="",description="品質チェックの理由")

class Judgement(BaseModel):
    current_judge: bool = Field(...,description="判定結果")
    reason: str = Field(...,description="判定理由")