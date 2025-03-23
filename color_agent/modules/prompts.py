from langchain_core.prompts import ChatPromptTemplate

purpose_prompt = ChatPromptTemplate.from_template("""
以下のユーザー要求を読み取り、次の観点で分析してください：
- 雰囲気・感情（tone）
- 使用場面（user_context）
- 想定ユーザー層（target_user）
- 色の使用目的（emotion） 

ユーザーの要求:'''{user_query}'''
""".strip())

suggestion_prompt = ChatPromptTemplate.from_template("""
あなたはUIデザイン向けのメインカラーの提案をするエージェントです。
以下の要求の分析結果に対して、色の提案をしてください。
提案は、色のコード、色の名前、色の理由を含めて3つ提示してください。

【分析結果】:'''
- 雰囲気・感情（tone）: {tone}
- UIの使用場面（user_context）: {user_context}
- 想定ユーザー層（target_user）: {target_user}
- 色の心理効果（emotion）: {emotion}
'''
""".strip())

check_prompt = ChatPromptTemplate.from_template("""
以下はユーザーの質問と、それに対する色の提案です。
この提案の品質をチェックしてください。

- 提案が3つあり、それぞれ色コード、名前、理由が含まれているか。
- 色がユーザーの要求（雰囲気・用途・感情）に合っているか。
- 不適切な点があれば指摘してください。

問題がある場合には'False'、問題がない場合には'True'を返答してください。また、その判断理由も返答してください。

ユーザーの質問: {query}
色の提案:
{suggestions}
""".strip())