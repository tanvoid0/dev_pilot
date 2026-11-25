from __future__ import annotations

try:
    import httpx
except ImportError:
    raise ImportError("Please install httpx with 'pip install httpx' ")


class Translator:
    @staticmethod
    async def translate(word: str):
        """Looks up a word."""
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            try:
                results = response.json()
            except Exception:
                return response.text
        return results