from langchain_core.language_models import BaseChatModel
from langchain_core.vectorstores import VectorStore
from langchain_core.prompts import PromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.output_parsers import BaseOutputParser
from typing import TypedDict, Set
import logging

logger = logging.getLogger(__name__)

class QAResponse(TypedDict):
    answer: str
    Sources: Set[str]
    
class ChatBot:
    """
    A ChatBot that orchestrates a QA chain using injected components.
    """
    def __init__(
        self, 
        llm: BaseChatModel, 
        vector_store: VectorStore, 
        prompt: PromptTemplate,
        parser:BaseOutputParser
    ):
        # Dependencies are "injected" here
        self.llm = llm
        self.vector_store = vector_store
        self.prompt = prompt
        self.parser = parser
        
        # The chain is built once during initialization
        self.qa_chain = self._build_qa_chain()

    def _build_qa_chain(self):
        """Builds the retrieval QA chain from the provided components."""
        logger.info("Building the QA chain...")
        doc_chain = create_stuff_documents_chain(self.llm, self.prompt,output_parser=self.parser)
        retrieval_chain = create_retrieval_chain(self.vector_store.as_retriever(), doc_chain)
        logger.info("QA chain is ready.")

        return retrieval_chain

    async def aask_question(self, query: str) -> QAResponse:
        """Asks a question using the pre-built QA chain."""
        if self.qa_chain is None:
            raise RuntimeError("The QA chain has not been built correctly.")
        
        result =await self.qa_chain.ainvoke({"input": query})
        sources = {source for doc in result['context'] if (source := doc.metadata.get('source')) is not None}

        return {'answer': result["answer"], 'Sources': sources}