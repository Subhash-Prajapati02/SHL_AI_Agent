import json
import os

from langchain_core.documents import Document

from langchain_community.document_loaders import (
    TextLoader
)


class DocumentLoader:

    def __init__(self):

        self.catalog_path = (
            "catalog/shl_catalog.json"
        )

        self.conversation_path = (
            "GenAI_SampleConversations"
        )
        
    def load_catalog(self):

        documents = []

        with open(
            self.catalog_path,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        for item in data:

            skills = ", ".join(
                item.get("skills", [])
            )

            languages = ", ".join(
                item.get("languages", [])
            )

            content = f"""
            Assessment Name:
            {item.get('name')}

            Description:
            {item.get('description')}

            Duration:
            {item.get('duration')}

            Skills:
            {skills}

            Languages:
            {languages}

            URL:
            {item.get('url')}
            """

            doc = Document(

                page_content=content,

                metadata={

                    "source":
                        str(
                            item.get("name", "")
                        ),

                    "url":
                        str(
                            item.get("url", "")
                        ),

                    "type":
                        "catalog",

                    "category":
                        str(skills),

                    "languages":
                        str(languages),

                    "duration":
                        str(
                            item.get(
                                "duration",
                                ""
                            )
                        )
                }
            )

            documents.append(doc)

        print(
            f"Catalog loaded: {len(documents)}"
        )

        return documents

    def load_markdown(self):

        documents = []

        files = os.listdir(
            self.conversation_path
        )

        for file in files:

            if file.endswith(".md"):

                path = os.path.join(
                    self.conversation_path,
                    file
                )

                loader = TextLoader(
                    path,
                    encoding="utf-8"
                )

                docs = loader.load()

                for doc in docs:

                    doc.metadata["source"] = (
                        str(file)
                    )

                    doc.metadata["type"] = (
                        "conversation_trace"
                    )

                documents.extend(docs)

        print(
            f"Markdown loaded: {len(documents)}"
        )

        return documents

    def load_all_documents(self):

        catalog_docs = self.load_catalog()

        markdown_docs = self.load_markdown()

        all_docs = (
            catalog_docs + markdown_docs
        )

        print(
            f"Total docs loaded: {len(all_docs)}"
        )

        return all_docs