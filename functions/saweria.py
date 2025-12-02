import requests

def saweria_qris(
    name: str,
    message: str,
    amount: int,
):
    url = f"https://backend.saweria.co/donations/snap/364898dc-ad7a-4f28-95c5-e04760df1296"

    payload = {
        "agree": True,
        "notUnderage": True,
        "message": message,
        "amount": str(amount),
        "payment_type": "qris",
        "vote": "",
        "currency": "IDR",
        "customer_info": {
            "first_name": name,
            "email": "m.zidanea.j@gmail.com",
            "phone": ""
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Origin": "https://saweria.co",
        "Referer": "https://saweria.co/",
        "User-Agent": "Mozilla/5.0",
    }

    res = requests.post(url, json=payload, headers=headers)

    return res.json()