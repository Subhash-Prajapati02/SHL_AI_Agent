import chromadb


class VectorDB:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="./chromadb_store"
        )

        self.collection = (
            self.client.get_or_create_collection(
                name="shl_collection"
            )
        )

    def add_documents(

        self,
        documents,
        embeddings,
        metadatas,
        ids
    ):

        self.collection.add(

            documents=documents,

            embeddings=embeddings,

            metadatas=metadatas,

            ids=ids
        )

    def query(

        self,
        embedding,
        top_k=5
    ):

        results = self.collection.query(

            query_embeddings=embedding,

            n_results=top_k
        )

        return results

    def count(self):

        return self.collection.count()