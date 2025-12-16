# 测试 LangChain 导入是否真的失败
try:
    from langchain_community.chat_models import ChatOpenAI
    from langchain_core.prompts import PromptTemplate  # 0.3.x 版本正确路径
    print("✅ 导入成功！LangChain 安装正常")
except ImportError as e:
    print(f"❌ 导入失败：{e}")