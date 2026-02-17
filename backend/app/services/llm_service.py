from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from enum import Enum
import asyncio

from app.core.config import settings


class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class LLMService:
    """
    Optimized LLM service for low latency production usage.
    """

    # 🔹 Clientes en memoria compartida (CRÍTICO)
    _openai_client: AsyncOpenAI | None = None
    _anthropic_client: AsyncAnthropic | None = None

    def __init__(self, provider: str = None):
        self.provider = provider or settings.LLM_PROVIDER

        if self.provider == LLMProvider.OPENAI:
            if LLMService._openai_client is None:
                LLMService._openai_client = AsyncOpenAI(
                    api_key=settings.OPENAI_API_KEY,
                    timeout=20,  # evita bloqueos eternos
                )
            self.client = LLMService._openai_client
            self.model = settings.LLM_MODEL

        elif self.provider == LLMProvider.ANTHROPIC:
            if LLMService._anthropic_client is None:
                LLMService._anthropic_client = AsyncAnthropic(
                    api_key=settings.ANTHROPIC_API_KEY,
                    timeout=20,
                )
            self.client = LLMService._anthropic_client
            self.model = "claude-3-5-sonnet-20241022"

        else:
            raise ValueError(f"Unknown LLM provider: {self.provider}")

    async def generate(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = None,
        max_tokens: int = None,
    ) -> str:
        """
        Generate response with timeout + low-latency defaults.
        """

        temperature = temperature or settings.LLM_TEMPERATURE or 0.2
        max_tokens = max_tokens or settings.LLM_MAX_TOKENS or 400

        try:
            # ⏱️ Timeout global de seguridad
            return await asyncio.wait_for(
                self._generate_internal(prompt, system_prompt, temperature, max_tokens),
                timeout=25,
            )
        except asyncio.TimeoutError:
            return "⚠️ La respuesta está tardando demasiado. Intenta reformular la pregunta."
        except Exception:
            return "⚠️ Error generando respuesta del modelo."

    async def _generate_internal(
        self,
        prompt: str,
        system_prompt: str,
        temperature: float,
        max_tokens: int,
    ) -> str:

        # ===== OPENAI (rápido) =====
        if self.provider == LLMProvider.OPENAI:
            messages = []

            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})

            messages.append({"role": "user", "content": prompt})

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            return response.choices[0].message.content.strip()

        # ===== ANTHROPIC =====
        elif self.provider == LLMProvider.ANTHROPIC:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system_prompt or "",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
            )

            return response.content[0].text.strip()

        else:
            raise ValueError(f"Unknown LLM provider: {self.provider}")
