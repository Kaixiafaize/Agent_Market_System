import os
import datetime
import pdfkit
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI  # 社区版模型（含第三方LLM）
from langchain_core.prompts import PromptTemplate  # 核心Prompt模块（路径不变）
from sqlmodel import Session
from src.core.celery import celery
from src.database.session import engine
from src.model.paper_task import PaperTask

load_dotenv()

# --------------------------
# 核心修改：适配硅基流动 API
# --------------------------
llm = ChatOpenAI(
    model_name=os.getenv("SILICONFLOW_MODEL"),  # 硅基流动模型名
    openai_api_base=os.getenv("SILICONFLOW_API_BASE"),  # 硅基流动API地址
    openai_api_key=os.getenv("SILICONFLOW_API_KEY"),  # 硅基流动API Key
    temperature=0.7,  # 生成温度
    max_tokens=4000,  # 最大生成字数，根据需求调整
)

# 论文生成 Prompt（保持不变，硅基流动模型兼容 LangChain Prompt）
PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["topic"],
    template="""
    请根据主题生成一篇结构完整的学术论文，包含标题、摘要、引言、研究方法、实验结果、讨论、结论、参考文献（至少3篇，GB/T 7714格式），输出为Markdown格式。
    主题：{topic}
    """
)

# Celery 异步任务（完全不变，逻辑复用）
@celery.task(bind=True, max_retries=1)
def generate_paper_task(self, task_id: str, topic: str):
    with Session(engine) as db:
        task = db.get(PaperTask, task_id)
        if not task:
            return "任务不存在"
        
        try:
            task.status = "running"
            db.add(task)
            db.commit()

            # 调用硅基流动模型生成论文
            chain = PROMPT_TEMPLATE | llm
            response = chain.invoke({"topic": topic})
            md_content = response.content

            # PDF 转换（不变）
            output_dir = "./generated_papers"
            os.makedirs(output_dir, exist_ok=True)
            pdf_path = f"{output_dir}/paper_{task_id}.pdf"
            pdfkit.from_string(md_content, pdf_path, options={"encoding": "UTF-8"})

            # 更新任务状态（不变）
            task.status = "completed"
            task.file_path = pdf_path
            task.completed_at = datetime.datetime.utcnow()
            db.add(task)
            db.commit()

            return pdf_path

        except Exception as e:
            task.status = "failed"
            db.add(task)
            db.commit()
            raise self.retry(exc=e, countdown=5)