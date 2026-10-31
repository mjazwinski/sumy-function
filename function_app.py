import azure.functions as func
import logging
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

app = func.FunctionApp()


@app.mcp_tool()
@app.mcp_tool_property(
    arg_name="text",
    description="Text to summarize"
)
def summarizer_mcp(text: str) -> str:
    """
    Sample function for text summarization
    """

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    senteces = LsaSummarizer()(parser.document, 2)
    
    logging.info("Code review checklist prompt invoked.")

    summary = str()
    return summary.join(senteces)
