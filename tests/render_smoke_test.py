import time
import requests


BASE_URL = "https://repg-product-sales-quote-api.onrender.com"

SUPER_ADMIN_EMAIL = "admin@repg.com.tr"
SUPER_ADMIN_PASSWORD = "ChangeThisNow123!"


def check_response(response, expected_status, label):
    if response.status_code != expected_status:
        print(f"FAIL: {label}")
        print(f"Expected: {expected_status}")
        print(f"Actual: {response.status_code}")
        print(response.text)
        raise SystemExit(1)

    print(f"PASS: {label}")


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def login(email, password):
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": email,
            "password": password,
        },
        timeout=30,
    )
    check_response(response, 200, f"login {email}")
    return response.json()["access_token"]


def main():
    timestamp = int(time.time())

    user_email = f"smoke.user.{timestamp}@example.com"
    product_sku = f"SMOKE-{timestamp}"

    response = requests.get(f"{BASE_URL}/", timeout=30)
    check_response(response, 200, "root endpoint")

    super_token = login(SUPER_ADMIN_EMAIL, SUPER_ADMIN_PASSWORD)

    response = requests.post(
        f"{BASE_URL}/products/",
        json={
            "name": "Smoke Test Product",
            "description": "Created by automated smoke test",
            "price": 1000,
            "currency": "EUR",
            "sku": product_sku,
            "category": "energy",
            "subcategory": "generator",
            "product_type": "standard",
            "stock_status": "in_stock",
            "lead_time": "7 days",
            "technical_specs": {
                "power": "5 kW",
                "voltage": "220V",
            },
            "is_active": True,
        },
        headers=auth_headers(super_token),
        timeout=30,
    )
    check_response(response, 200, "create product")
    product_id = response.json()["id"]

    response = requests.post(
        f"{BASE_URL}/users/",
        json={
            "full_name": "Smoke Test User",
            "email": user_email,
            "password": "ChangeThisNow123!",
            "company_name": "Smoke Test Company",
        },
        timeout=30,
    )
    check_response(response, 200, "create regular user")

    user_token = login(user_email, "ChangeThisNow123!")

    response = requests.post(
        f"{BASE_URL}/quotes/",
        json={
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 1,
                }
            ]
        },
        headers=auth_headers(user_token),
        timeout=30,
    )
    check_response(response, 200, "create quote")
    quote_id = response.json()["id"]

    response = requests.patch(
        f"{BASE_URL}/quotes/{quote_id}/status",
        params={"status_value": "approved"},
        headers=auth_headers(super_token),
        timeout=30,
    )
    check_response(response, 200, "approve quote")

    response = requests.post(
        f"{BASE_URL}/orders/from-quote/{quote_id}",
        headers=auth_headers(super_token),
        timeout=30,
    )
    check_response(response, 200, "create order from quote")
    order_id = response.json()["id"]

    response = requests.get(
        f"{BASE_URL}/orders/my",
        headers=auth_headers(user_token),
        timeout=30,
    )
    check_response(response, 200, "get my orders")

    order_ids = [order["id"] for order in response.json()]

    if order_id not in order_ids:
        print("FAIL: created order not found in user's orders")
        raise SystemExit(1)

    print("PASS: created order found in user's orders")
    print("ALL SMOKE TESTS PASSED")


if __name__ == "__main__":
    main()
