import uuid

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from rag.loader import (
    DocumentLoader
)

from rag.embedder import (
    Embedder
)

from rag.vectordb import (
    VectorDB
)


class RAG_Pipeline:

    def __init__(self):

        self.loader = DocumentLoader()

        self.embedder = Embedder()

        self.vectordb = VectorDB()

    def chunk_documents(

        self,
        docs
    ):

        splitter = (
            RecursiveCharacterTextSplitter(

                chunk_size=500,

                chunk_overlap=50
            )
        )

        chunks = splitter.split_documents(
            docs
        )

        return chunks

    def create_vector_database(

        self,
        chunks
    ):

        if self.vectordb.count() > 0:

            print(
                "Database already exists"
            )

            return

        texts = [

            chunk.page_content

            for chunk in chunks
        ]

        metadatas = [

            chunk.metadata

            for chunk in chunks
        ]

        print(
            "Creating embeddings..."
        )

        embeddings = self.embedder.encode(
            texts
        )

        ids = [

            str(uuid.uuid4())

            for _ in range(len(texts))
        ]

        print(
            "Saving vectors..."
        )

        self.vectordb.add_documents(

            documents=texts,

            embeddings=embeddings,

            metadatas=metadatas,

            ids=ids
        )

        print(
            "Vector DB Created"
        )

    def run(self):

        if self.vectordb.count() > 0:

            print(
                "Database already exists"
            )

            print(
                f"Total vectors: "
                f"{self.vectordb.count()}"
            )

            return

        print(
            "Loading documents..."
        )

        docs = (
            self.loader.load_all_documents()
        )

        print(
            f"Documents Loaded: "
            f"{len(docs)}"
        )

        chunks = self.chunk_documents(
            docs
        )

        print(
            f"Chunks Created: "
            f"{len(chunks)}"
        )

        self.create_vector_database(
            chunks
        )

        print(
            f"Total vectors: "
            f"{self.vectordb.count()}"
        )

    def retrieve(

        self,
        question,
        top_k=5
    ):
        
        if self.vectordb.count() == 0:

            return (
                "No documents found "
                "in database."
            )

        query_embedding = (
            self.embedder.encode(
                [question]
            )
        )

        results = self.vectordb.query(

            embedding=query_embedding,

            top_k=top_k
        )

        docs = results["documents"][0]

        metas = results["metadatas"][0]

        context_parts = []

        for i in range(len(docs)):

            source = metas[i].get(

                "source",

                "unknown"
            )

            text = docs[i]

            context_parts.append(

                f"Source: {source}\n\n{text}"
            )

        context = "\n\n".join(
            context_parts
        )

        return context