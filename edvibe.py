"""
Edvibe API integration.

Edvibe does not have a public API spec — replace the logic inside
`register_student` with the real endpoint and payload once you get
the API credentials from Edvibe support.
"""

import secrets
import string
import aiohttp
from config import EDVIBE_API_URL, EDVIBE_API_KEY, EDVIBE_COURSE_ID


def _generate_password(length: int = 10) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


async def register_student(user_id: int, first_name: str, last_name: str) -> tuple[str, str]:
    """
    Registers a student in Edvibe and returns (login, password).

    Replace the body of this function with the real Edvibe API call.
    """
    login = f"user{user_id}"
    password = _generate_password()

    # ── Real API call (fill in when Edvibe provides endpoint docs) ─────────
    # payload = {
    #     "email": f"{login}@rusglobal.bot",
    #     "password": password,
    #     "first_name": first_name,
    #     "last_name": last_name,
    #     "course_id": EDVIBE_COURSE_ID,
    # }
    # headers = {"Authorization": f"Bearer {EDVIBE_API_KEY}"}
    # async with aiohttp.ClientSession() as session:
    #     async with session.post(f"{EDVIBE_API_URL}/students", json=payload, headers=headers) as resp:
    #         if resp.status not in (200, 201):
    #             text = await resp.text()
    #             raise RuntimeError(f"Edvibe API error {resp.status}: {text}")
    #         data = await resp.json()
    #         login = data.get("login", login)
    # ───────────────────────────────────────────────────────────────────────

    return login, password
