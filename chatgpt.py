import openai

openai.api_key = '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'

model_engine = "text-davinci-003"
prompt = str(input())

completion = openai.Completion.create(
    engine = model_engine,
    prompt = prompt,
    max_tokens = 1024,n=1,
    stop=None,temperature=0.5,
)

response = completion.choices[0].text
print(response)