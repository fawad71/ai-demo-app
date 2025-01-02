from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

reflection_chain = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a viral twitter influencer that is trying to get more followers. You are given a tweet and you need to reflect on it and provide recommendations for improvement including hashtags, images, and other content.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a twitter techie influencer assistant tasked with generating an excellent tweitter posts. generate the best possible twitter post possible for user request. If the user provides critical feedback, you should reflect on it and provide revised version of your previous response.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

generation_chain = generation_prompt | llm
reflection_chain = reflection_chain | llm
