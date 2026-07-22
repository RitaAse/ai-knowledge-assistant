class FakeLLMResponse:

    def __init__(self, content: str):
        self.content = content



class FakeLLM:

    def invoke(self, prompt: str):

        return FakeLLMResponse(
            "The recommended operating system is Windows 11."
        )