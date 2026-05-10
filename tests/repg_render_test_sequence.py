import time
import requests


BASE_URL = "https://repg-product-sales-quote-api.onrender.com"

SUPER_ADMIN_EMAIL = "admin@repg.com.tr"
SUPER_ADMIN_PASSWORD = "ChangeThisNow123!"

TEST_PASSWORD = "ChangeThisNow123!"
TIMEOUT = 30


class ApiTester:
    def __init__(self):
        self.timestamp = int(time.time())

        self.super_admin_token = None
        self.admin_token = None
        self.user_token = None
        self.user_2_token = None

        self.product_id = None
        self.product_id_2 = None
        self.quote_id = None
        self.quote_id_2 = None
        self.order_id = None
        self.order_id_2 = None

        self.user_email = f"repg.test.customer.{self.timestamp}@example.com"
        self.user_2_email = f"repg.test.customer2.{self.timestamp}@example.com"
        self.admin_email = f"repg.test.admin.{self.timestamp}@example.com"

        self.product_sku = f"REPG-SMOKE-001-{self.timestamp}"
        self.product_sku_2 = f"REPG-SMOKE-002-{self.timestamp}"

        self.feature_results = {}
        self.current_feature = None

    def headers(self, token):
        return {"Authorization": f"Bearer {token}"}

    def start_feature(self, feature_name):
        self.current_feature = feature_name

        if feature_name not in self.feature_results:
            self.feature_results[feature_name] = {
                "passed": True,
                "failed_endpoints": [],
                "skipped_steps": [],
            }

    def fail_feature(self, method, path, label, status_code, response_text):
        if not self.current_feature:
            return

        self.feature_results[self.current_feature]["passed"] = False
        self.feature_results[self.current_feature]["failed_endpoints"].append(
            {
                "method": method,
                "path": path,
                "label": label,
                "status_code": status_code,
                "response_text": response_text,
            }
        )

    def skip_feature(self, reason):
        if not self.current_feature:
            return

        self.feature_results[self.current_feature]["passed"] = False
        self.feature_results[self.current_feature]["skipped_steps"].append(reason)

        print(f"SKIP: {self.current_feature}")
        print(f"Reason: {reason}")

    def request(
        self,
        method,
        path,
        label,
        expected_status=200,
        token=None,
        json=None,
        params=None,
    ):
        headers = self.headers(token) if token else None

        try:
            response = requests.request(
                method=method,
                url=f"{BASE_URL}{path}",
                json=json,
                params=params,
                headers=headers,
                timeout=TIMEOUT,
            )
        except requests.RequestException as error:
            self.fail_feature(method, path, label, "REQUEST_ERROR", str(error))
            print(f"FAIL: {label}")
            print(error)
            return None

        if response.status_code != expected_status:
            self.fail_feature(
                method,
                path,
                label,
                response.status_code,
                response.text,
            )

            print(f"FAIL: {label}")
            print(f"Expected: {expected_status}")
            print(f"Actual: {response.status_code}")
            print(response.text)
            return None

        print(f"PASS: {label}")

        if response.text:
            try:
                return response.json()
            except ValueError:
                return response.text

        return None

    def login(self, email, password, label):
        data = self.request(
            "POST",
            "/auth/login",
            label,
            json={
                "email": email,
                "password": password,
            },
        )

        if not isinstance(data, dict):
            return None

        token = data.get("access_token")

        if not token:
            self.fail_feature(
                "POST",
                "/auth/login",
                label,
                "NO_TOKEN",
                "Response did not include access_token",
            )
            print(f"FAIL: {label} did not return access_token")
            return None

        return token

    def assert_field(self, data, field, expected, label):
        if not isinstance(data, dict):
            self.fail_feature(
                "ASSERT",
                field,
                label,
                "INVALID_DATA",
                "Response was not a JSON object",
            )
            print(f"FAIL: {label}")
            return False

        actual = data.get(field)

        if actual != expected:
            self.fail_feature(
                "ASSERT",
                field,
                label,
                "ASSERTION_FAILED",
                f"Expected {field}: {expected}, actual {field}: {actual}",
            )
            print(f"FAIL: {label}")
            print(f"Expected {field}: {expected}")
            print(f"Actual {field}: {actual}")
            return False

        print(f"PASS: {label}")
        return True

    def assert_id_in_list(self, items, item_id, label):
        if not isinstance(items, list):
            self.fail_feature(
                "ASSERT",
                "list",
                label,
                "INVALID_DATA",
                "Response was not a JSON list",
            )
            print(f"FAIL: {label}")
            return False

        ids = [item.get("id") for item in items if isinstance(item, dict)]

        if item_id not in ids:
            self.fail_feature(
                "ASSERT",
                "list",
                label,
                "ASSERTION_FAILED",
                f"Missing id: {item_id}",
            )
            print(f"FAIL: {label}")
            print(f"Missing id: {item_id}")
            return False

        print(f"PASS: {label}")
        return True

    def test_root_endpoint(self):
        self.start_feature("root endpoint")
        self.request("GET", "/", "root endpoint")

    def test_super_admin_login(self):
        self.start_feature("super admin login")
        self.super_admin_token = self.login(
            SUPER_ADMIN_EMAIL,
            SUPER_ADMIN_PASSWORD,
            "login as initial super admin",
        )

    def test_jwt_authorization(self):
        self.start_feature("JWT authorization")

        if not self.super_admin_token:
            self.skip_feature("super_admin_token is missing")
            return

        self.request(
            "GET",
            "/auth/me",
            "JWT-protected endpoint accepts Bearer token",
            token=self.super_admin_token,
        )

    def test_auth_me_super_admin(self):
        self.start_feature("/auth/me")

        if not self.super_admin_token:
            self.skip_feature("super_admin_token is missing")
            return

        data = self.request(
            "GET",
            "/auth/me",
            "verify super admin identity",
            token=self.super_admin_token,
        )

        self.assert_field(data, "role", "super_admin", "super admin role check")

    def test_product_create_list_filter_get_update(self):
        self.start_feature("product create/list/filter/get/update")

        if not self.super_admin_token:
            self.skip_feature("super_admin_token is missing")
            return

        data = self.request(
            "POST",
            "/products/",
            "create first product as super admin",
            token=self.super_admin_token,
            json={
                "name": "RePG Automated Test Product 1",
                "description": "Initial product created by automated API test",
                "price": 1100,
                "currency": "EUR",
                "sku": self.product_sku,
                "category": "energy",
                "subcategory": "generator",
                "product_type": "standard",
                "stock_status": "in_stock",
                "stock_quantity": 10,
                "lead_time": "7 days",
                "technical_specs": {
                    "power": "5 kW",
                    "voltage": "220V",
                },
                "is_active": True,
            },
        )

        if isinstance(data, dict):
            self.product_id = data.get("id")

        self.request("GET", "/products/", "list products without filters")

        self.request(
            "GET",
            "/products/",
            "list products with filters",
            params={
                "category": "energy",
                "stock_status": "in_stock",
            },
        )

        if not self.product_id:
            self.skip_feature("product_id is missing after product creation")
            return

        data = self.request(
            "GET",
            f"/products/{self.product_id}",
            "get first product",
        )

        self.assert_field(data, "id", self.product_id, "first product id check")

        data = self.request(
            "PUT",
            f"/products/{self.product_id}",
            "update first product",
            token=self.super_admin_token,
            json={
                "name": "RePG Automated Test Product 1 Updated",
                "description": "Updated product by automated API test",
                "price": 1250,
                "currency": "EUR",
                "sku": self.product_sku,
                "category": "energy",
                "subcategory": "generator",
                "product_type": "standard",
                "stock_status": "in_stock",
                "stock_quantity": 10,
                "lead_time": "10 days",
                "technical_specs": {
                    "power": "6 kW",
                    "voltage": "230V",
                },
                "is_active": True,
            },
        )

        self.assert_field(
            data,
            "name",
            "RePG Automated Test Product 1 Updated",
            "first product update check",
        )

    def test_public_user_registration(self):
        self.start_feature("public user registration")

        self.request(
            "POST",
            "/users/",
            "create first regular user",
            json={
                "full_name": "RePG Test Customer 1",
                "email": self.user_email,
                "password": TEST_PASSWORD,
                "company_name": "RePG Automated Test Company",
            },
        )

    def test_regular_user_login(self):
        self.start_feature("regular user login")

        self.user_token = self.login(
            self.user_email,
            TEST_PASSWORD,
            "login as first regular user",
        )

    def test_regular_user_product_browsing(self):
        self.start_feature("regular user product browsing")

        if not self.product_id:
            self.skip_feature("product_id is missing")
            return

        self.request("GET", "/products/", "regular user lists products")

        data = self.request(
            "GET",
            f"/products/{self.product_id}",
            "regular user gets first product",
        )

        self.assert_field(
            data,
            "id",
            self.product_id,
            "regular user first product id check",
        )

    def test_quote_creation(self):
        self.start_feature("quote creation")

        if not self.user_token:
            self.skip_feature("user_token is missing")
            return

        if not self.product_id:
            self.skip_feature("product_id is missing")
            return

        data = self.request(
            "POST",
            "/quotes/",
            "create first quote",
            token=self.user_token,
            json={
                "items": [
                    {
                        "product_id": self.product_id,
                        "quantity": 1,
                    }
                ]
            },
        )

        if isinstance(data, dict):
            self.quote_id = data.get("id")

    def test_own_quote_retrieval(self):
        self.start_feature("own quote retrieval")

        if not self.user_token:
            self.skip_feature("user_token is missing")
            return

        if not self.quote_id:
            self.skip_feature("quote_id is missing")
            return

        data = self.request(
            "GET",
            "/quotes/my",
            "get own quotes",
            token=self.user_token,
        )

        self.assert_id_in_list(
            data,
            self.quote_id,
            "first quote appears in own quotes",
        )

    def test_single_quote_retrieval(self):
        self.start_feature("single quote retrieval")

        if not self.user_token:
            self.skip_feature("user_token is missing")
            return

        if not self.quote_id:
            self.skip_feature("quote_id is missing")
            return

        data = self.request(
            "GET",
            f"/quotes/{self.quote_id}",
            "get first quote by id",
            token=self.user_token,
        )

        self.assert_field(data, "id", self.quote_id, "first quote id check")

    def test_super_admin_quote_approval(self):
        self.start_feature("super admin quote approval")

        if not self.super_admin_token:
            self.skip_feature("super_admin_token is missing")
            return

        if not self.quote_id:
            self.skip_feature("quote_id is missing")
            return

        self.request(
            "PATCH",
            f"/quotes/{self.quote_id}/status",
            "approve first quote",
            token=self.super_admin_token,
            params={"status_value": "approved"},
        )

    def test_order_creation_from_approved_quote(self):
        self.start_feature("order creation from approved quote")

        if not self.super_admin_token:
            self.skip_feature("super_admin_token is missing")
            return

        if not self.quote_id:
            self.skip_feature("quote_id is missing")
            return

        data = self.request(
            "POST",
            f"/orders/from-quote/{self.quote_id}",
            "create first order from quote",
            token=self.super_admin_token,
        )

        if isinstance(data, dict):
            self.order_id = data.get("id")

    def test_regular_user_own_order_retrieval(self):
        self.start_feature("regular user own order retrieval")

        if not self.user_token:
            self.skip_feature("user_token is missing")
            return

        if not self.order_id:
            self.skip_feature("order_id is missing")
            return

        data = self.request(
            "GET",
            "/orders/my",
            "get own orders",
            token=self.user_token,
        )

        self.assert_id_in_list(
            data,
            self.order_id,
            "first order appears in own orders",
        )

    def test_single_order_retrieval(self):
        self.start_feature("single order retrieval")

        if not self.user_token:
            self.skip_feature("user_token is missing")
            return

        if not self.order_id:
            self.skip_feature("order_id is missing")
            return

        data = self.request(
            "GET",
            f"/orders/{self.order_id}",
            "get first order by id",
            token=self.user_token,
        )

        self.assert_field(data, "id", self.order_id, "first order id check")

    def test_internal_admin_creation(self):
        self.start_feature("internal admin creation")

        if not self.super_admin_token:
            self.skip_feature("super_admin_token is missing")
            return

        data = self.request(
            "POST",
            "/admin/users/",
            "create internal admin user",
            token=self.super_admin_token,
            json={
                "full_name": "RePG Test Internal Admin",
                "email": self.admin_email,
                "password": TEST_PASSWORD,
                "company_name": "RePG Automated Test Company",
                "role": "admin",
            },
        )

        self.assert_field(data, "role", "admin", "internal admin role check")

    def test_admin_login(self):
        self.start_feature("admin login")

        self.admin_token = self.login(
            self.admin_email,
            TEST_PASSWORD,
            "login as internal admin",
        )

        if not self.admin_token:
            return

        data = self.request(
            "GET",
            "/auth/me",
            "verify internal admin identity",
            token=self.admin_token,
        )

        self.assert_field(data, "role", "admin", "admin role check")

    def test_admin_product_management(self):
        self.start_feature("admin product management")

        if not self.admin_token:
            self.skip_feature("admin_token is missing")
            return

        data = self.request(
            "POST",
            "/products/",
            "create second product as admin",
            token=self.admin_token,
            json={
                "name": "RePG Automated Test Product 2",
                "description": "Second product created by automated API test",
                "price": 2100,
                "currency": "EUR",
                "sku": self.product_sku_2,
                "category": "energy",
                "subcategory": "industrial",
                "product_type": "standard",
                "stock_status": "in_stock",
                "stock_quantity": 10,
                "lead_time": "14 days",
                "technical_specs": {
                    "power": "10 kW",
                    "voltage": "400V",
                },
                "is_active": True,
            },
        )

        if isinstance(data, dict):
            self.product_id_2 = data.get("id")

        self.request("GET", "/products/", "admin lists products")

        if not self.product_id_2:
            self.skip_feature("product_id_2 is missing after second product creation")
            return

        data = self.request(
            "GET",
            f"/products/{self.product_id_2}",
            "admin gets second product",
        )

        self.assert_field(data, "id", self.product_id_2, "second product id check")

        data = self.request(
            "PUT",
            f"/products/{self.product_id_2}",
            "admin updates second product",
            token=self.admin_token,
            json={
                "name": "RePG Automated Test Product 2 Updated",
                "description": "Second product updated by automated API test",
                "price": 2200,
                "currency": "EUR",
                "sku": self.product_sku_2,
                "category": "energy",
                "subcategory": "industrial",
                "product_type": "standard",
                "stock_status": "in_stock",
                "stock_quantity": 10,
                "lead_time": "21 days",
                "technical_specs": {
                    "power": "12 kW",
                    "voltage": "400V",
                },
                "is_active": True,
            },
        )

        self.assert_field(
            data,
            "name",
            "RePG Automated Test Product 2 Updated",
            "second product update check",
        )

    def test_second_user_quote_flow(self):
        self.start_feature("second user quote flow")

        if not self.product_id_2:
            self.skip_feature("product_id_2 is missing")
            return

        self.request(
            "POST",
            "/users/",
            "create second regular user",
            json={
                "full_name": "RePG Test Customer 2",
                "email": self.user_2_email,
                "password": TEST_PASSWORD,
                "company_name": "RePG Automated Test Company",
            },
        )

        self.user_2_token = self.login(
            self.user_2_email,
            TEST_PASSWORD,
            "login as second regular user",
        )

        if not self.user_2_token:
            self.skip_feature("user_2_token is missing")
            return

        data = self.request(
            "POST",
            "/quotes/",
            "create second quote",
            token=self.user_2_token,
            json={
                "items": [
                    {
                        "product_id": self.product_id_2,
                        "quantity": 2,
                    }
                ]
            },
        )

        if isinstance(data, dict):
            self.quote_id_2 = data.get("id")

        if not self.quote_id_2:
            self.skip_feature("quote_id_2 is missing after second quote creation")

    def test_admin_quote_approval(self):
        self.start_feature("admin quote approval")

        if not self.admin_token:
            self.skip_feature("admin_token is missing")
            return

        if not self.quote_id_2:
            self.skip_feature("quote_id_2 is missing")
            return

        self.request(
            "PATCH",
            f"/quotes/{self.quote_id_2}/status",
            "admin approves second quote",
            token=self.admin_token,
            params={"status_value": "approved"},
        )

    def test_admin_order_creation(self):
        self.start_feature("admin order creation")

        if not self.admin_token:
            self.skip_feature("admin_token is missing")
            return

        if not self.quote_id_2:
            self.skip_feature("quote_id_2 is missing")
            return

        data = self.request(
            "POST",
            f"/orders/from-quote/{self.quote_id_2}",
            "admin creates second order from quote",
            token=self.admin_token,
        )

        if isinstance(data, dict):
            self.order_id_2 = data.get("id")

    def test_admin_list_users(self):
        self.start_feature("admin list users")

        if not self.admin_token:
            self.skip_feature("admin_token is missing")
            return

        self.request(
            "GET",
            "/users/",
            "admin lists users",
            token=self.admin_token,
        )

    def test_admin_list_all_quotes(self):
        self.start_feature("admin list all quotes")

        if not self.admin_token:
            self.skip_feature("admin_token is missing")
            return

        self.request(
            "GET",
            "/quotes/",
            "admin lists all quotes",
            token=self.admin_token,
        )

    def test_admin_list_all_orders(self):
        self.start_feature("admin list all orders")

        if not self.admin_token:
            self.skip_feature("admin_token is missing")
            return

        self.request(
            "GET",
            "/orders/",
            "admin lists all orders",
            token=self.admin_token,
        )

    def print_feature_summary(self):
        print("")
        print("DEPLOYED RENDER BACKEND FEATURE SUPPORT SUMMARY")
        print("")

        for feature_name, result in self.feature_results.items():
            if result["passed"]:
                print(
                    "PASS: deployed Render backend currently supports "
                    f"{feature_name}"
                )
            else:
                print(
                    "FAIL: deployed Render backend currently does not support "
                    f"{feature_name}"
                )

                if result["failed_endpoints"]:
                    print("Related failed endpoints:")

                    for failed in result["failed_endpoints"]:
                        print(
                            f"- {failed['method']} {failed['path']} - "
                            f"{failed['label']} - status {failed['status_code']}"
                        )
                        print(f"  Response: {failed['response_text']}")

                if result["skipped_steps"]:
                    print("Related skipped steps:")

                    for skipped in result["skipped_steps"]:
                        print(f"- {skipped}")

                print("")

    def print_test_data_summary(self):
        print("")
        print("TEST DATA CREATED")
        print(f"USER 1 EMAIL: {self.user_email}")
        print(f"USER 2 EMAIL: {self.user_2_email}")
        print(f"ADMIN EMAIL: {self.admin_email}")
        print(f"PRODUCT SKU 1: {self.product_sku}")
        print(f"PRODUCT SKU 2: {self.product_sku_2}")
        print(f"PRODUCT ID 1: {self.product_id}")
        print(f"PRODUCT ID 2: {self.product_id_2}")
        print(f"QUOTE ID 1: {self.quote_id}")
        print(f"QUOTE ID 2: {self.quote_id_2}")
        print(f"ORDER ID 1: {self.order_id}")
        print(f"ORDER ID 2: {self.order_id_2}")

    def print_final_status(self):
        failed = [
            feature_name
            for feature_name, result in self.feature_results.items()
            if not result["passed"]
        ]

        print("")

        if failed:
            print("TEST SEQUENCE FINISHED WITH FAILURES")
            print(f"FAILED FEATURE COUNT: {len(failed)}")
        else:
            print("ALL TEST SEQUENCE CHECKS PASSED")

    def run(self):
        print("STARTING REPG API TEST SEQUENCE")
        print(f"BASE_URL: {BASE_URL}")
        print(f"TEST RUN ID: {self.timestamp}")
        print("")

        self.test_root_endpoint()
        self.test_super_admin_login()
        self.test_jwt_authorization()
        self.test_auth_me_super_admin()
        self.test_product_create_list_filter_get_update()
        self.test_public_user_registration()
        self.test_regular_user_login()
        self.test_regular_user_product_browsing()
        self.test_quote_creation()
        self.test_own_quote_retrieval()
        self.test_single_quote_retrieval()
        self.test_super_admin_quote_approval()
        self.test_order_creation_from_approved_quote()
        self.test_regular_user_own_order_retrieval()
        self.test_single_order_retrieval()
        self.test_internal_admin_creation()
        self.test_admin_login()
        self.test_admin_product_management()
        self.test_second_user_quote_flow()
        self.test_admin_quote_approval()
        self.test_admin_order_creation()
        self.test_admin_list_users()
        self.test_admin_list_all_quotes()
        self.test_admin_list_all_orders()

        self.print_feature_summary()
        self.print_final_status()
        self.print_test_data_summary()


if __name__ == "__main__":
    tester = ApiTester()
    tester.run()
