import logging
import threading

from nltk.tokenize import word_tokenize
from callGPT3 import gpt35_text, gpt35_text_stream
from datetime import datetime
from LoggerFactory import create_logger


SYSTEM_ROLE = "system"
ASSISTANT_ROLE = "assistant"
USER_ROLE = "user"

class AgentSettings:
    def __init__(self, system_prompt, filename_prefix = "agent", gpt_max_reply_tokens = 500, max_session_memory = 2500, gpt_temperature = 1.0, gpt_max_total_tokens = 4096):
        self.gpt_max_reply_tokens = gpt_max_reply_tokens
        self.gpt_max_total_tokens = gpt_max_total_tokens
        self.gpt_temperature = gpt_temperature
        self.system_prompt = system_prompt
        self.filename_prefix = filename_prefix
        self.max_session_memory = max_session_memory

class GPT35Agent:
    def __init__(self, agent_settings):
        self.agent_settings = agent_settings
        self.current_result = ""
        self.current_result_complete = True

        self.messages = []
        self.system_message = self.create_message(ASSISTANT_ROLE, agent_settings.system_prompt)
        self.system_message_world_length = len(word_tokenize(self.system_message["content"]))
        
        logger_name = f"GPT35Agent.{agent_settings.filename_prefix}"
        self.logger = create_logger(logger_name, level=logging.INFO, filename_prefix=agent_settings.filename_prefix)

        self.log_message(self.system_message)

    def log_message(self, message):
        self.logger.info("\n---\n{}: {}\n".format(message["role"].capitalize(), message["content"]))

    def step_session(self):
        self.messages.insert(0, self.system_message)
        max_reply_tokens = self.calc_max_reply_token_count()
        print("max reply tokens: {}".format(max_reply_tokens))
        response = gpt35_text(self.messages, self.agent_settings.gpt_temperature, max_reply_tokens)
        self.messages.pop(0)
        self.add_message(ASSISTANT_ROLE, response)
        return response

    def calc_max_reply_token_count(self):
        request_tokens = self.get_word_count() + self.system_message_world_length
        if request_tokens + self.agent_settings.gpt_max_reply_tokens > self.agent_settings.gpt_max_total_tokens:
            return self.agent_settings.gpt_max_total_tokens - request_tokens
        else:
            return self.agent_settings.gpt_max_reply_tokens

    def process_stream(self, response_stream):
        self.current_result = ""
        self.current_result_complete = False

        # Iterate through the stream of events
        for chunk in response_stream:
            chunk_message = chunk['choices'][0]['delta']
            self.current_result += chunk_message.get('content', '')

        self.add_message(ASSISTANT_ROLE, self.current_result)
        self.current_result_complete = True

    def step_session_stream(self):
        self.messages.insert(0, self.system_message)
        max_reply_tokens = self.calc_max_reply_token_count()
        print("max reply tokens: {}".format(max_reply_tokens))
        response_stream = gpt35_text_stream(self.messages, self.agent_settings.gpt_temperature, max_reply_tokens)
        self.messages.pop(0)

        thread = threading.Thread(target=self.process_stream, args=(response_stream,))
        thread.start()

    def step_session_stream2(self):
        self.messages.insert(0, self.system_message)
        max_reply_tokens = self.calc_max_reply_token_count()
        print("max reply tokens: {}".format(max_reply_tokens))
        response_stream = gpt35_text_stream(self.messages, self.agent_settings.gpt_temperature, max_reply_tokens)
        self.messages.pop(0)

        self.current_result = ""
        for chunk in response_stream:
            chunk_message = chunk['choices'][0]['delta']
            content = chunk_message.get('content', '')
            self.current_result += content
            yield content

        self.add_message(ASSISTANT_ROLE, self.current_result)
        self.current_result_complete = True

    def get_current_result(self):
        return self.current_result

    def get_current_result_complete(self):
        return self.current_result_complete

    def add_user_message(self, text):
        self.add_message(USER_ROLE, text)

    def add_assistant_message(self, text):
        self.add_message(ASSISTANT_ROLE, text)

    def checkMessagesLength(self):
        word_count = self.get_word_count()
        print(f"\nWord count: {word_count} Msg Count: {len(self.messages)}")

        while word_count > self.agent_settings.max_session_memory:
            self.messages.pop(0)
            word_count = self.get_word_count()
            print(f"Reduced word count: {word_count} Msg Count: {len(self.messages)}")

    def get_word_count(self):
        return sum(len(word_tokenize(message['content'])) for message in self.messages) + self.system_message_world_length

    def create_message(self, role, content):
        return { "role": role, "content": content }

    def add_message(self, role, content):
        message = self.create_message(role, content)
        self.messages.append(message)
        self.log_message(message)
        self.checkMessagesLength()

    def clear_messages(self):
        self.messages = []

    def set_system_message(self, prompt, role = SYSTEM_ROLE):
        self.system_message = self.create_message(role, prompt)

