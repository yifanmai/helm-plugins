from typing import List, Dict

from helm.common.cache import Cache, CacheConfig
from helm.common.request import Request, RequestResult, Sequence, Token
from helm.common.tokenization_request import (
    DecodeRequest,
    DecodeRequestResult,
    TokenizationRequest,
    TokenizationRequestResult,
    TokenizationToken,
)
from helm.proxy.clients.client import Client, wrap_request_time


class PluginDemoClient(Client):
    """Implements some "models" that just generate silly things quickly just to debug the infrastructure."""

    def __init__(self, cache_config: CacheConfig):
        self.cache = Cache(cache_config)

    @staticmethod
    def tokenize_by_space(text: str) -> List[str]:
        """Simply tokenizes by a single white space."""
        return text.split(" ")

    def make_request(self, request: Request) -> RequestResult:
        raw_request = {
            "engine": request.model_engine,
            "prompt": request.prompt,
            "n": request.num_completions,
        }

        def do_it():
            return self.invoke_model1(raw_request)

        cache_key = Client.make_cache_key(raw_request, request)
        response, cached = self.cache.get(cache_key, wrap_request_time(do_it))
        completions = [
            Sequence(
                text=text,
                logprob=logprob,
                tokens=[Token(text=text, logprob=logprob, top_logprobs=response["completions"])],
            )
            for text, logprob in response["completions"].items()
        ]

        return RequestResult(
            success=True,
            cached=cached,
            request_time=0,
            request_datetime=response.get("request_datetime"),
            completions=completions,
            embedding=[],
        )

    def tokenize(self, request: TokenizationRequest) -> TokenizationRequestResult:
        raw_tokens: List[str] = PluginDemoClient.tokenize_by_space(request.text)
        return TokenizationRequestResult(
            success=True, cached=False, tokens=[TokenizationToken(text) for text in raw_tokens], text=request.text
        )

    def decode(self, request: DecodeRequest) -> DecodeRequestResult:
        raise NotImplementedError

    def invoke_model1(self, raw_request: Dict) -> Dict:
        """
        Example: 7 2 4 6
        Completions (num_completions = 3):
        - 6
        - 4
        - 2
        """
        prompt_tokens: List[str] = PluginDemoClient.tokenize_by_space(raw_request["prompt"])
        choices = reversed(prompt_tokens[-raw_request["n"] :])
        response = {"completions": dict((text, -i) for i, text in enumerate(choices))}
        return response
