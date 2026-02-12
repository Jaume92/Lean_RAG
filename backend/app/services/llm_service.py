from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from enum import Enum
from app.core.config import settings

class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"

class LLMService:
    """
    Service for interacting with different LLM providers
    """
    
    def __init__(self, provider: str = None):
        self.provider = provider or settings.LLM_PROVIDER
        
        if self.provider == LLMProvider.OPENAI:
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            self.model = settings.LLM_MODEL
        elif self.provider == LLMProvider.ANTHROPIC:
            self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
            self.model = "claude-3-5-sonnet-20241022"
    
    async def generate(
        self, 
        prompt: str, 
        system_prompt: str = None,
        temperature: float = None,
        max_tokens: int = None
    ) -> str:
        """
        Generate response from LLM
        
        Args:
            prompt: User prompt
            system_prompt: System instructions
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        temperature = temperature or settings.LLM_TEMPERATURE
        max_tokens = max_tokens or settings.LLM_MAX_TOKENS
        
        if self.provider == LLMProvider.OPENAI:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        
        elif self.provider == LLMProvider.ANTHROPIC:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system_prompt or "",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature
            )
            return response.content[0].text
        
        else:
            raise ValueError(f"Unknown LLM provider: {self.provider}")
    
    async def generate_structured(self, prompt: str, response_format: dict):
        """
        Generate structured JSON response
        
        Note: This uses function calling for structured outputs
        """
        # TODO: Implement function calling for structured outputs
        pass
