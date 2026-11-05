from __future__ import annotations

import os
import time
import json
import logging
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Carregar variáveis do .env
load_dotenv()

logger = logging.getLogger(__name__)


class GeminiClient:
    """
    Wrapper Gemini via Vertex AI.
    Compatível com a estratégia atual do projeto.
    Requer:
        gcloud auth application-default login
    """

    DEFAULT_PROJECT = os.getenv(
        "VERTEX_PROJECT",
        os.getenv("GCP_PROJECT"),
    )

    DEFAULT_LOCATION = os.getenv(
        "VERTEX_LOCATION",
        os.getenv("GCP_LOCATION", "global"),
    )

    DEFAULT_MODEL = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.6-flash",
    )

    def __init__(
        self,
        project: str | None = None,
        location: str | None = None,
        model: str | None = None,
        temperature: float = 0.0,
        max_retries: int = 5,
    ):
        self.project = project or self.DEFAULT_PROJECT
        self.location = location or self.DEFAULT_LOCATION
        self.model = model or self.DEFAULT_MODEL
        self.temperature = temperature
        self.max_retries = max_retries

        logger.info(
            "Inicializando Gemini (project=%s, location=%s, model=%s)",
            self.project,
            self.location,
            self.model,
        )

        # Se houver GEMINI_API_KEY no .env, usamos a inicialização convencional (API Key do AI Studio)
        # Se não houver, ou se USE_VERTEX_AI=true, inicializa via Vertex AI com vertexai=True
        api_key = os.getenv("GEMINI_API_KEY")
        use_vertex = os.getenv("USE_VERTEX_AI", "true").lower() == "true"

        if use_vertex or not api_key:
            self.client = genai.Client(
                vertexai=True,
                project=self.project,
                location=self.location,
            )
        else:
            self.client = genai.Client(api_key=api_key)

        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def _generate(
        self,
        contents: list[Any],
        system_prompt: str | None = None,
        temperature: float | None = None,
        response_mime_type: str | None = None,
        model: str | None = None,
    ):
        config = types.GenerateContentConfig(
            temperature=(
                self.temperature
                if temperature is None
                else temperature
            ),
        )

        if system_prompt:
            config.system_instruction = system_prompt

        if response_mime_type:
            config.response_mime_type = response_mime_type

        last_error: Exception | None = None
        target_model = model or self.model
        
        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=target_model,
                    contents=contents,
                    config=config,
                )
                if response.usage_metadata:
                    self.total_input_tokens += getattr(response.usage_metadata, "prompt_token_count", 0)
                    self.total_output_tokens += getattr(response.usage_metadata, "candidates_token_count", 0)
                return response
            except Exception as exc:
                last_error = exc
                logger.warning(
                    "Erro Gemini (tentativa %s/%s): %s",
                    attempt,
                    self.max_retries,
                    exc,
                )
                if attempt < self.max_retries:
                    time.sleep(min(attempt * 2, 10))
        raise last_error

    def generate_text_with_metadata(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float | None = None,
        model: str | None = None,
    ) -> tuple[str, int, int, int]:
        """
        Gera resposta em texto e retorna também metadados da chamada individual.
        Retorna: (texto_resposta, tokens_entrada, tokens_saida, tokens_totais)
        """
        response = self._generate(
            contents=[prompt],
            system_prompt=system_prompt,
            temperature=temperature,
            model=model,
        )

        t_in = 0
        t_out = 0
        t_tot = 0

        if response.usage_metadata:
            t_in = getattr(response.usage_metadata, "prompt_token_count", 0) or 0
            t_out = getattr(response.usage_metadata, "candidates_token_count", 0) or 0
            t_tot = getattr(response.usage_metadata, "total_token_count", 0) or 0

        return (response.text or "").strip(), t_in, t_out, t_tot


# Cliente padrão compartilhado para chamadas rápidas
_default_client = None

def get_client() -> GeminiClient:
    global _default_client
    if _default_client is None:
        _default_client = GeminiClient()
    return _default_client

def gerar_resposta(prompt, model="gemini-3.6-flash", temperature=0.0):
    """
    Função base utilizada pelo harness de testes (runner e estratégias).
    Encapsula o uso resiliente do GeminiClient.
    """
    client = get_client()
    # Força a utilização do modelo configurado no runner ou herda o gemini-3.6-flash
    return client.generate_text_with_metadata(prompt, model=model, temperature=temperature)

