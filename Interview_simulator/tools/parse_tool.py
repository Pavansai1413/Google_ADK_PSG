from google.adk.tools import FunctionTool
from .document_parser import parse_document

parse_document_tool = FunctionTool(parse_document)