from langchain_llm import get_langchain_llm


llm = get_langchain_llm()

response = llm.invoke("Give one safe Linux command to check disk usage.")

print(response.content)