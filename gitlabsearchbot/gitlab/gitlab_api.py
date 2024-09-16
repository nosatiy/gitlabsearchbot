import httpx
import logging

from settings import settings
from httpx import TimeoutException

logger = logging.getLogger(__name__)


class GitGraphQL:

    def __init__(self):
        self.url = f"{settings.git_url}/api/graphql"
        self.headers = {
            "Authorization": "Bearer " + settings.git_token
        }
        self.async_client = None

    async def async_post(self, query_body: str, timeout: int = 100):
        try:
            resp = await self.async_client.post(
                url=self.url, json={"query": query_body}, timeout=timeout
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get("errors"):
                    logger.error(data.get("errors"))
                    return None
                return data["data"]
            else:
                logger.error(str(resp.status_code))
                return None
        except TimeoutException as error:
            logger.error(error)
            return None

    async def create_session(self):
        self.async_client = httpx.AsyncClient(headers=self.headers)
        
    async def close_session(self):
        try:
            await self.async_client.aclose()
        except:
            logger.warning('apparently the client is closed')

    async def reconnect(self):
        await self.close_session()
        await self.create_session()


