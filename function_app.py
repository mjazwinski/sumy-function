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
@app.mcp_tool_property(
    arg_name="sentence_count",
    description="Number of sentences to put into summary. Default: 6.",
    is_required=False
)
def summarizer_mcp(text: str, sentence_count: int = 6) -> str:
    """
    Sample function for text summarization
    """

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    sentences = LsaSummarizer()(parser.document, sentence_count)
    
    logging.info("Code review checklist prompt invoked.")
    
    return str().join([str(setnence) for setnence in sentences])
