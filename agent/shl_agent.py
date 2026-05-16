from langchain_groq import ChatGroq

from rag.rag_pipeline import (
    RAG_Pipeline
)

from rag.prompts import (
    SYSTEM_PROMPT
)

from dotenv import load_dotenv

import os


load_dotenv()


class SHLAgent:

    def __init__(self):

        self.rag = RAG_Pipeline()

        self.rag.run()

        self.llm = ChatGroq(

            groq_api_key=os.getenv(
                "API_KEY"
            ),

            model=
                "llama-3.1-8b-instant",

            temperature=0.2,

            max_tokens=1024
        )

    def is_off_topic(

        self,
        text
    ):

        off_topics = [

            "football",

            "movie",

            "politics",

            "religion",

            "cricket",

            "fifa",

            "ipl",

            "netflix",

            "actor"
        ]

        text = text.lower()

        for word in off_topics:

            if word in text:

                return True

        return False

    def is_comparison_query(

        self,
        text
    ):

        compare_words = [

            "compare",

            "difference",

            "vs",

            "versus"
        ]

        text = text.lower()

        for word in compare_words:

            if word in text:

                return True

        return False

    def is_vague_query(

        self,
        text
    ):

        text = text.lower()

        technical_keywords = [

            "python",

            "java",

            "react",

            "spring",

            "flask",

            "django",

            "sql",

            "aws",

            "docker",

            "kubernetes",

            "machine learning",

            "data science",

            "api",

            "frontend",

            "backend",

            "cybersecurity",

            "networking"
        ]

        for word in technical_keywords:

            if word in text:

                return False

        if len(text.split()) <= 3:

            return True

        generic_queries = [

            "need assessment",

            "recommend assessment",

            "need hiring test",

            "need developer assessment",

            "need engineer assessment"
        ]

        for query in generic_queries:

            if query in text:

                return True

        return False

    def clarification_question(

        self,
        text
    ):

        return (
            "Could you share more details "
            "about the role, skills, "
            "seniority level, or "
            "assessment type you need?"
        )

    def compare_assessments(

        self,
        question
    ):

        context = self.rag.retrieve(
            question
        )

        prompt = f"""
        {SYSTEM_PROMPT}

        Compare the assessments
        clearly using ONLY the
        provided context.

        Context:
        {context}

        User Question:
        {question}
        """

        response = self.llm.invoke(
            prompt
        )

        return {

            "reply":
                response.content,

            "recommendations":
                [],

            "end_of_conversation":
                False
        }

    def recommend_assessments(

        self,
        question
    ):

        context = self.rag.retrieve(
            question
        )

        prompt = f"""
        {SYSTEM_PROMPT}

        You are an SHL assessment
        recommendation assistant.

        Recommend only assessments
        from the provided context.

        Return:
        - assessment names
        - why recommended
        - duration
        - skills
        - SHL URLs

        Context:
        {context}

        User Requirement:
        {question}
        """

        response = self.llm.invoke(
            prompt
        )

        recommendations = []

        lines = context.split("\n")

        current_name = ""
        current_url = ""

        for line in lines:

            if "Assessment Name:" in line:

                current_name = (
                    line.replace(
                        "Assessment Name:",
                        ""
                    ).strip()
                )

            if "URL:" in line:

                current_url = (
                    line.replace(
                        "URL:",
                        ""
                    ).strip()
                )

                if current_name:

                    recommendations.append({

                        "name":
                            current_name,

                        "url":
                            current_url,

                        "test_type":
                            "K"
                    })

            if len(recommendations) >= 5:

                break

        return {

            "reply":
                response.content,

            "recommendations":
                recommendations,

            "end_of_conversation":
                True
        }

    def ask(

        self,
        conversation
    ):

        if self.is_off_topic(
            conversation
        ):

            return {

                "reply":
                    "I can only help "
                    "with SHL assessment "
                    "recommendations.",

                "recommendations":
                    [],

                "end_of_conversation":
                    False
            }

        if self.is_comparison_query(
            conversation
        ):

            return self.compare_assessments(
                conversation
            )

        if self.is_vague_query(
            conversation
        ):

            return {

                "reply":
                    self.clarification_question(
                        conversation
                    ),

                "recommendations":
                    [],

                "end_of_conversation":
                    False
            }
        
        return self.recommend_assessments(
            conversation
        )