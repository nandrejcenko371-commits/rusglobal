import hashlib
from config import (
    ROBOKASSA_LOGIN, ROBOKASSA_PASSWORD1, ROBOKASSA_PASSWORD2,
    ROBOKASSA_TEST_MODE, MARATHON_DESCRIPTION,
)


def _md5(s: str) -> str:
    return hashlib.md5(s.encode("utf-8")).hexdigest().upper()


def generate_payment_url(user_id: int, price: float) -> str:
    inv_id = user_id
    out_sum = f"{price:.2f}"
    sig = _md5(f"{ROBOKASSA_LOGIN}:{out_sum}:{inv_id}:{ROBOKASSA_PASSWORD1}")

    params = (
        f"MerchantLogin={ROBOKASSA_LOGIN}"
        f"&OutSum={out_sum}"
        f"&InvId={inv_id}"
        f"&Description={MARATHON_DESCRIPTION}"
        f"&SignatureValue={sig}"
        f"&IsTest={ROBOKASSA_TEST_MODE}"
        f"&Encoding=utf-8"
    )
    return f"https://auth.robokassa.ru/Merchant/Index.aspx?{params}"


def verify_result_signature(out_sum: str, inv_id: str, sig: str) -> bool:
    expected = _md5(f"{out_sum}:{inv_id}:{ROBOKASSA_PASSWORD2}")
    return expected == sig.upper()
