from openai import OpenAI
import helperFunctions as hf

env = hf.loadEnv()

client = OpenAI(
    api_key=env["OPEN_API"]
)

try:
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
        ]
    )
except Exception as e:
    print(f'Failed: \n{e}')
    exit()

print(completion.choices[0].message)