import os
import openai
import time

openai.api_key = os.getenv('OPENAI_API_KEY')

def gpt3_all(prompt, max_tokens=3500, temperature=0.0):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response

def gpt3_text(prompt, max_tokens=3500, temperature=0.0):
    return gpt3_all(prompt, max_tokens=max_tokens, temperature=temperature).choices[0].text


def gpt3_text_prompt_all(prompt, text_chunks, max_tokens=3500, temperature=0.0):
    responses = []
    for i, chunk in enumerate(text_chunks):
        gpt_prompt = f"{prompt}{chunk}"
        print("Getting response for chunk: ", i)
        gpt_response = gpt3_text(gpt_prompt, max_tokens, temperature)
        responses.append(gpt_response)
    return responses


def gpt35_all(messages, temperature = 0.0, max_tokens=None):
    retry_count = 10
    for i in range(0,retry_count):
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model = "gpt-3.5-turbo",
                    messages = messages,
                    temperature = temperature,
                    max_tokens = max_tokens,
                 #   presence_penalty = 0.5,
                 #   frequency_penalty = 0.5,
                )
                return response
            except Exception as e:
                # Retry the function after a delay if the API returns an error
                print(f"API Error: {e}")
                print(f"Retrying {i+1} time(s) in 10 seconds...")
                time.sleep(10)
                continue
            break

def gpt35_text(messages, temperature = 0.0, max_tokens=None):
    return gpt35_all(messages, temperature).choices[0]['message']['content']



def gpt35_text_stream(messages, temperature = 0.0, max_tokens=None):
    retry_count = 10
    for i in range(0,retry_count):
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model = "gpt-3.5-turbo",
                    messages = messages,
                    temperature = temperature,
                    max_tokens = max_tokens,
                 #   presence_penalty = 0.5,
                 #   frequency_penalty = 0.5,
                    stream = True,
                )
                return response
            except Exception as e:
                # Retry the function after a delay if the API returns an error
                print(f"API Error: {e}")
                print(f"Retrying {i+1} time(s) in 10 seconds...")
                time.sleep(10)
                continue
            break


# messages=[
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "Knock knock."},
#     {"role": "assistant", "content": "Who's there?"},
#     {"role": "user", "content": "Orange."},
# ]

# response = gpt35_all(messages)

# print(response);
