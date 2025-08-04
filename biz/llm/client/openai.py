import os
from typing import Dict, List, Optional

from openai import OpenAI

from biz.llm.client.base import BaseClient
from biz.llm.types import NotGiven, NOT_GIVEN


from biz.utils.default_config import get_env_with_default
from biz.utils.log import logger


class OpenAIClient(BaseClient):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or get_env_with_default("OPENAI_API_KEY")
        self.base_url = get_env_with_default("OPENAI_API_BASE_URL")
        if not self.api_key:
            raise ValueError("API key is required. Please provide it or set it in the environment variables.")

        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        self.default_model = get_env_with_default("OPENAI_API_MODEL")

    def completions(self,
                    messages: List[Dict[str, str]],
                    model: Optional[str] | NotGiven = NOT_GIVEN,
                    ) -> str:
        try:
            model = model or self.default_model
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
            )
            
            if not completion or not completion.choices:
                return "OpenAI API服务返回为空，请稍后重试"
                
            return completion.choices[0].message.content
            
        except Exception as e:
            # 检查是否是认证错误
            if "401" in str(e):
                return "OpenAI API认证失败，请检查API密钥是否正确"
            elif "404" in str(e):
                return "OpenAI API接口未找到，请检查API地址是否正确"
            else:
                return f"调用OpenAI API时出错: {str(e)}"
