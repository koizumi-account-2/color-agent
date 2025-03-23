from color_agent.modules.agent import ColorAgent
from color_agent.modules.config import model

def main():
    agent = ColorAgent(model)
    result = agent.run("社内で使うシステムです。使用者は社員です。見ていて落ち着く色を提案してください")
    print("result",result)
    print("最終提案:", result['suggestions'][-1])
    print("品質チェック:", result['judge_reason'])

if __name__ == "__main__":
    main()

