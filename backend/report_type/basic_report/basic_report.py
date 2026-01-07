from fastapi import WebSocket
from typing import Any
import os

from gpt_researcher import GPTResearcher
from gpt_researcher.actions.business_prompt import build_business_custom_prompt


class BasicReport:
    def __init__(
        self,
        query: str,
        query_domains: list,
        report_type: str,
        report_source: str,
        source_urls,
        document_urls,
        tone: Any,
        config_path: str,
        websocket: WebSocket,
        headers=None,
        mcp_configs=None,
        mcp_strategy=None,
    ):
        self.query = query
        self.query_domains = query_domains
        self.report_type = report_type
        self.report_source = report_source
        self.source_urls = source_urls
        self.document_urls = document_urls
        self.tone = tone
        self.config_path = config_path
        self.websocket = websocket
        self.headers = headers or {}

        # Initialize researcher with optional MCP parameters
        gpt_researcher_params = {
            "query": self.query,
            "query_domains": self.query_domains,
            "report_type": self.report_type,
            "report_source": self.report_source,
            "source_urls": self.source_urls,
            "document_urls": self.document_urls,
            "tone": self.tone,
            "config_path": self.config_path,
            "websocket": self.websocket,
            "headers": self.headers,
        }

        # Add MCP parameters if provided
        if mcp_configs is not None:
            gpt_researcher_params["mcp_configs"] = mcp_configs
        if mcp_strategy is not None:
            gpt_researcher_params["mcp_strategy"] = mcp_strategy

        self.gpt_researcher = GPTResearcher(**gpt_researcher_params)

    async def run(self):
        await self.gpt_researcher.conduct_research()
        # Business-focused custom prompt injection (no template change)
        business_mode = os.getenv("BUSINESS_MODE", "true").lower() == "true"
        custom_prompt = ""
        if business_mode:
            # Parse hints from headers if provided via frontend
            user_inputs = {}
            try:
                if isinstance(self.headers, dict):
                    region = self.headers.get("business_region") or ""
                    customer = self.headers.get("business_customer") or ""
                    competitors = self.headers.get("business_competitors") or ""
                    if competitors and isinstance(competitors, str):
                        competitors_list = [c.strip() for c in competitors.split(",") if c.strip()]
                    else:
                        competitors_list = competitors if isinstance(competitors, list) else []
                    user_inputs = {
                        "region": region,
                        "customer": customer,
                        "competitors": competitors_list,
                    }
            except Exception:
                user_inputs = {}
            custom_prompt = build_business_custom_prompt(self.query, user_inputs)

        report = await self.gpt_researcher.write_report(custom_prompt=custom_prompt)
        return report
