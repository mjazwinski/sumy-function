import azure.functions as func
import logging
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

app = func.FunctionApp(http_auth_level=func.AuthLevel.SYSTEM)

@app.mcp_prompt_trigger(
    arg_name="context",
    prompt_name="code_review_checklist",
    description="Returns a structured code review checklist prompt for evaluating code changes."
)
def summarizer_mcp(context: func.PromptInvocationContext) -> str:
    """
    Sample function for text summarization
    """
    text = """
    AI is transforming industries.
    Machine learning learns from data.
    AI improves healthcare.
    """

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summary = LsaSummarizer()(parser.document, 2)
    logging.info("Code review checklist prompt invoked.")

    # get token from 
    
    return summary
