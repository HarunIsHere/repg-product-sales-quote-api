import { useEffect, useMemo, useState } from "react";
import "./App.css";

const API_BASE = "https://api.ayartuerk.me";

const text = {
  en: {
    portal: "Product & Quote Portal",
    language: "EN",
    otherLanguage: "TR",
    nav: {
      home: "Home",
      products: "Products",
      quotes: "Quotes",
      orders: "Orders",
      admin: "Admin",
      api: "API",
      dashboard: "Dashboard",
      login: "Login",
      register: "Register",
      logout: "Logout",
    },
    heroTitle: "Clean technology product and quote management portal.",
    heroText:
      "Browse products, request quotes, track orders, and operate role-based backend workflows from one frontend.",
    loginTitle: "Login",
    registerTitle: "Register",
    dashboardTitle: "Dashboard",
    email: "Email",
    password: "Password",
    fullName: "Full name",
    companyName: "Company name",
    submitLogin: "Login",
    submitRegister: "Register",
    currentUser: "Current user",
    role: "Role",
    notLoggedIn: "Not logged in",
    openSwagger: "Open Swagger",
    endpointPanel: "Endpoint Access Panel",
    response: "Response",
    loadProducts: "Load Products",
    createQuote: "Create Quote",
    productId: "Product ID",
    quantity: "Quantity",
    quoteId: "Quote ID",
    orderId: "Order ID",
    statusValue: "Status",
    createOrder: "Create Order From Quote",
    updateQuoteStatus: "Update Quote Status",
    loadMyQuotes: "Load My Quotes",
    loadMyOrders: "Load My Orders",
    loadAllQuotes: "Load All Quotes",
    loadAllOrders: "Load All Orders",
    createInternalUser: "Create Internal User",
    userRole: "User role",
    adminOnly: "Admin / super_admin only",
    customerTools: "Customer Tools",
    adminTools: "Admin Tools",
    publicTools: "Public Tools",
  },
  tr: {
    portal: "Ürün ve Teklif Portalı",
    language: "TR",
    otherLanguage: "EN",
    nav: {
      home: "Ana Sayfa",
      products: "Ürünler",
      quotes: "Teklifler",
      orders: "Siparişler",
      admin: "Admin",
      api: "API",
      dashboard: "Panel",
      login: "Giriş",
      register: "Kayıt",
      logout: "Çıkış",
    },
    heroTitle: "Temiz teknoloji ürün ve teklif yönetim portalı.",
    heroText:
      "Ürünleri inceleyin, teklif isteyin, siparişleri takip edin ve rol bazlı backend iş akışlarını tek frontend üzerinden kullanın.",
    loginTitle: "Giriş",
    registerTitle: "Kayıt",
    dashboardTitle: "Panel",
    email: "Email",
    password: "Şifre",
    fullName: "Ad Soyad",
    companyName: "Şirket adı",
    submitLogin: "Giriş",
    submitRegister: "Kayıt",
    currentUser: "Mevcut kullanıcı",
    role: "Rol",
    notLoggedIn: "Giriş yapılmadı",
    openSwagger: "Swagger Aç",
    endpointPanel: "Endpoint Erişim Paneli",
    response: "Cevap",
    loadProducts: "Ürünleri Yükle",
    createQuote: "Teklif Oluştur",
    productId: "Ürün ID",
    quantity: "Miktar",
    quoteId: "Teklif ID",
    orderId: "Sipariş ID",
    statusValue: "Durum",
    createOrder: "Tekliften Sipariş Oluştur",
    updateQuoteStatus: "Teklif Durumunu Güncelle",
    loadMyQuotes: "Tekliflerimi Yükle",
    loadMyOrders: "Siparişlerimi Yükle",
    loadAllQuotes: "Tüm Teklifleri Yükle",
    loadAllOrders: "Tüm Siparişleri Yükle",
    createInternalUser: "İç Kullanıcı Oluştur",
    userRole: "Kullanıcı rolü",
    adminOnly: "Sadece admin / super_admin",
    customerTools: "Müşteri Araçları",
    adminTools: "Admin Araçları",
    publicTools: "Public Araçlar",
  },
};

function getLanguage() {
  return window.location.pathname.startsWith("/tr") ? "tr" : "en";
}

function getPage() {
  const parts = window.location.pathname.split("/").filter(Boolean);
  return parts[1] || "home";
}

function getBase(language) {
  return `/${language}`;
}

async function apiRequest(path, options = {}, token = "") {
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(JSON.stringify(data || { detail: response.statusText }, null, 2));
  }

  return data;
}

function Header({ language, t, user, onLogout }) {
  const base = getBase(language);
  const otherBase = language === "en" ? "/tr/" : "/en/";

  return (
    <header className="site-header">
      <a className="brand" href={`${base}/`}>
        <div className="brand-mark">RePG</div>
        <div>
          <p className="brand-kicker">Renewable Energy Power Generation</p>
          <h1>{t.portal}</h1>
        </div>
      </a>

      <nav className="nav-links" aria-label="Main navigation">
        <a href={`${base}/`}>{t.nav.home}</a>
        <a href={`${base}/products`}>{t.nav.products}</a>
        <a href={`${base}/quotes`}>{t.nav.quotes}</a>
        <a href={`${base}/orders`}>{t.nav.orders}</a>
        <a href={`${base}/admin`}>{t.nav.admin}</a>
        <a href={`${base}/api`}>{t.nav.api}</a>
        <a href={`${base}/dashboard`}>{t.nav.dashboard}</a>
        {!user && <a href={`${base}/login`}>{t.nav.login}</a>}
        {!user && <a href={`${base}/register`}>{t.nav.register}</a>}
        {user && (
          <button className="nav-button" type="button" onClick={onLogout}>
            {t.nav.logout}
          </button>
        )}
        <a className="language-switch" href={otherBase}>
          {t.otherLanguage}
        </a>
      </nav>
    </header>
  );
}

function HomePage({ language, t }) {
  const base = getBase(language);

  return (
    <>
      <section className="hero-section">
        <div className="hero-content">
          <p className="section-label">RePG Portal</p>
          <h2>{t.heroTitle}</h2>
          <p className="hero-text">{t.heroText}</p>

          <div className="hero-actions">
            <a className="primary-button" href={`${base}/products`}>
              {t.nav.products}
            </a>
            <a className="secondary-button" href={`${API_BASE}/docs`}>
              {t.openSwagger}
            </a>
          </div>
        </div>

        <aside className="hero-card">
          <p>api.ayartuerk.me</p>
          <h3>Live Backend</h3>
          <span>FastAPI</span>
          <span>PostgreSQL</span>
          <span>JWT Auth</span>
          <span>Role-Based Access</span>
        </aside>
      </section>

      <section className="card-grid-section">
        <a className="feature-card" href={`${base}/products`}>
          <h3>{t.nav.products}</h3>
          <p>GET /products/ - GET /products/&#123;product_id&#125;</p>
          <span>Open →</span>
        </a>

        <a className="feature-card" href={`${base}/quotes`}>
          <h3>{t.nav.quotes}</h3>
          <p>POST /quotes/ - GET /quotes/my - GET /quotes/&#123;quote_id&#125;</p>
          <span>Open →</span>
        </a>

        <a className="feature-card" href={`${base}/orders`}>
          <h3>{t.nav.orders}</h3>
          <p>GET /orders/my - GET /orders/&#123;order_id&#125;</p>
          <span>Open →</span>
        </a>

        <a className="feature-card" href={`${base}/admin`}>
          <h3>{t.nav.admin}</h3>
          <p>Products, quotes, orders, and internal users.</p>
          <span>Open →</span>
        </a>
      </section>
    </>
  );
}

function LoginPage({ language, t, onLogin, setOutput }) {
  const [form, setForm] = useState({
    email: "",
    password: "",
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loginError, setLoginError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    setLoginError("");

    try {
      const tokenData = await apiRequest("/auth/login", {
        method: "POST",
        body: JSON.stringify(form),
      });

      localStorage.setItem("repg_token", tokenData.access_token);

      const userData = await apiRequest("/auth/me", {}, tokenData.access_token);
      onLogin(tokenData.access_token, userData);
      setOutput(userData);
      window.history.pushState({}, "", `${getBase(language)}/dashboard`);
      window.dispatchEvent(new PopStateEvent("popstate"));
    } catch {
      setLoginError("Invalid email or password");
      setOutput(null);
    }
  }

  return (
    <FormShell title={t.loginTitle}>
      <form className="form-card" onSubmit={handleSubmit}>
        {loginError && <p className="form-error">{loginError}</p>}

        <label>
          {t.email}
          <input
            type="email"
            value={form.email}
            onChange={(event) => setForm({ ...form, email: event.target.value })}
            required
          />
        </label>

        <label>
          {t.password}
          <div className="password-field">
            <input
              type={showPassword ? "text" : "password"}
              value={form.password}
              onChange={(event) => setForm({ ...form, password: event.target.value })}
              required
            />
            <button
              className="password-toggle"
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              aria-label={showPassword ? "Hide password" : "Show password"}
            >
              <span className={showPassword ? "eye-icon hidden" : "eye-icon"} />
            </button>
          </div>
        </label>

        <button className="primary-button" type="submit">
          {t.submitLogin}
        </button>
      </form>
    </FormShell>
  );
}

function RegisterPage({ t, setOutput }) {
  const [form, setForm] = useState({
    full_name: "",
    email: "",
    password: "",
    confirm_password: "",
    company_name: "",
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();

    if (form.password !== form.confirm_password) {
      setOutput("Passwords do not match.");
      return;
    }

    try {
      const data = await apiRequest("/users/", {
        method: "POST",
        body: JSON.stringify({
          full_name: form.full_name,
          email: form.email,
          password: form.password,
          company_name: form.company_name || null,
        }),
      });

      setOutput(data);
    } catch (error) {
      setOutput(error.message);
    }
  }

  return (
    <FormShell title={t.registerTitle}>
      <form className="form-card" onSubmit={handleSubmit}>
        <label>
          {t.fullName}
          <input
            value={form.full_name}
            onChange={(event) => setForm({ ...form, full_name: event.target.value })}
            required
          />
        </label>

        <label>
          {t.email}
          <input
            type="email"
            value={form.email}
            onChange={(event) => setForm({ ...form, email: event.target.value })}
            required
          />
        </label>

        <label>
          {t.password}
          <div className="password-field">
            <input
              type={showPassword ? "text" : "password"}
              value={form.password}
              onChange={(event) => setForm({ ...form, password: event.target.value })}
              required
            />
            <button
              className="password-toggle"
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              aria-label={showPassword ? "Hide password" : "Show password"}
            >
              <span className={showPassword ? "eye-icon hidden" : "eye-icon"} />
            </button>
          </div>
        </label>

        <label>
          Confirm password
          <div className="password-field">
            <input
              type={showConfirmPassword ? "text" : "password"}
              value={form.confirm_password}
              onChange={(event) =>
                setForm({ ...form, confirm_password: event.target.value })
              }
              required
            />
            <button
              className="password-toggle"
              type="button"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              aria-label={
                showConfirmPassword ? "Hide confirm password" : "Show confirm password"
              }
            >
              <span className={showConfirmPassword ? "eye-icon hidden" : "eye-icon"} />
            </button>
          </div>
        </label>

        <label>
          {t.companyName}
          <input
            value={form.company_name}
            onChange={(event) =>
              setForm({ ...form, company_name: event.target.value })
            }
          />
        </label>

        <button className="primary-button" type="submit">
          {t.submitRegister}
        </button>
      </form>
    </FormShell>
  );
}

function ProductsPage({ t, token, setOutput }) {
  async function loadProducts() {
    try {
      const data = await apiRequest("/products/?limit=100");
      setOutput(data);
    } catch (error) {
      setOutput(error.message);
    }
  }

  async function createDemoProduct() {
    try {
      const data = await apiRequest(
        "/products/",
        {
          method: "POST",
          body: JSON.stringify({
            name: "Demo Product",
            description: "Created from frontend",
            price: "100.00",
            currency: "EUR",
            sku: `DEMO-${Date.now()}`,
            category: "energy",
            subcategory: "demo",
            product_type: "system",
            stock_status: "available",
            stock_quantity: 10,
            lead_time: "2 weeks",
            technical_specs: {
              source: "frontend",
            },
            is_active: true,
          }),
        },
        token
      );

      setOutput(data);
    } catch (error) {
      setOutput(error.message);
    }
  }

  return (
    <ToolPage title={t.nav.products}>
      <ActionButton label="GET /products/" text={t.loadProducts} onClick={loadProducts} />
      <ActionButton
        label="POST /products/"
        text="Create demo product"
        onClick={createDemoProduct}
      />
    </ToolPage>
  );
}

function QuotesPage({ t, token, setOutput }) {
  const [form, setForm] = useState({
    product_id: "",
    quantity: 1,
    quote_id: "",
    status_value: "approved",
  });

  async function createQuote() {
    try {
      const data = await apiRequest(
        "/quotes/",
        {
          method: "POST",
          body: JSON.stringify({
            items: [
              {
                product_id: form.product_id,
                quantity: Number(form.quantity),
              },
            ],
          }),
        },
        token
      );

      setOutput(data);
    } catch (error) {
      setOutput(error.message);
    }
  }

  async function loadMyQuotes() {
    try {
      const data = await apiRequest("/quotes/my", {}, token);
      setOutput(data);
    } catch (error) {
      setOutput(error.message);
    }
  }

  async function loadAllQuotes() {
    try {
      const data = await apiRequest("/quotes/?limit=100", {}, token);
      setOutput(data);
    } catch (error) {
      setOutput(error.message);
    }
  }

  async function updateQuoteStatus() {
    try {
      const data = await apiRequest(
        `/quotes/${form.quote_id}/status?status_value=${form.status_value}`,
        {
          method: "PATCH",
        },
        token
      );

      setOutput(data);
    } catch (error) {
      setOutput(error.message);
    }
  }

  return (
    <ToolPage title={t.nav.quotes}>
      <div className="form-card compact">
        <label>
          {t.productId}
          <input
            value={form.product_id}
            onChange={(event) => setForm({ ...form, product_id: event.target.value })}
          />
        </label>

        <label>
          {t.quantity}
          <input
            type="number"
            min="1"
            value={form.quantity}
            onChange={(event) => setForm({ ...form, quantity: event.target.value })}
          />
        </label>

        <button className="primary-button" type="button" onClick={createQuote}>
          {t.createQuote}
        </button>
      </div>

      <ActionButton label="GET /quotes/my" text={t.loadMyQuotes} onClick={loadMyQuotes} />
      <ActionButton label="GET /quotes/" text={t.loadAllQuotes} onClick={loadAllQuotes} />

      <div className="form-card compact">
        <label>
          {t.quoteId}
          <input
            value={form.quote_id}
            onChange={(event) => setForm({ ...form, quote_id: event.target.value })}
          />
        </label>

        <label>
          {t.statusValue}
          <select
            value={form.status_value}
            onChange={(event) =>
              setForm({ ...form, status_value: event.target.value })
            }
          >
            <option value="pending">pending</option>
            <option value="approved">approved</option>
            <option value="rejected">rejected</option>
            <option value="converted">converted</option>
          </select>
        </label>

        <button className="primary-button" type="button" onClick={updateQuoteStatus}>
          {t.updateQuoteStatus}
        </button>
      </div>
    </ToolPage>
  );
}

function OrdersPage({ t, token, setOutput }) {
  const [quoteId, setQuoteId] = useState("");

  async function loadMyOrders() {
    try {
      const data = await apiRequest("/orders/my", {}, token);
      setOutput(data);
    } catch (error) {
      setOutput(error.message);
    }
  }

  async function loadAllOrders() {
    try {
      const data = await apiRequest("/orders/?limit=100", {}, token);
      setOutput(data);
    } catch (error) {
      setOutput(error.message);
    }
  }

  async function createOrder() {
    try {
      const data = await apiRequest(
        `/orders/from-quote/${quoteId}`,
        {
          method: "POST",
        },
        token
      );

      setOutput(data);
    } catch (error) {
      setOutput(error.message);
    }
  }

  return (
    <ToolPage title={t.nav.orders}>
      <ActionButton label="GET /orders/my" text={t.loadMyOrders} onClick={loadMyOrders} />
      <ActionButton label="GET /orders/" text={t.loadAllOrders} onClick={loadAllOrders} />

      <div className="form-card compact">
        <label>
          {t.quoteId}
          <input value={quoteId} onChange={(event) => setQuoteId(event.target.value)} />
        </label>

        <button className="primary-button" type="button" onClick={createOrder}>
          {t.createOrder}
        </button>
      </div>
    </ToolPage>
  );
}

function AdminPage({ t, token, setOutput }) {
  const [form, setForm] = useState({
    full_name: "",
    email: "",
    password: "",
    company_name: "",
    role: "admin",
  });

  async function createInternalUser() {
    try {
      const data = await apiRequest(
        "/admin/users/",
        {
          method: "POST",
          body: JSON.stringify({
            ...form,
            company_name: form.company_name || null,
          }),
        },
        token
      );

      setOutput(data);
    } catch (error) {
      setOutput(error.message);
    }
  }

  return (
    <ToolPage title={t.nav.admin}>
      <p className="muted">{t.adminOnly}</p>

      <div className="form-card compact">
        <label>
          {t.fullName}
          <input
            value={form.full_name}
            onChange={(event) => setForm({ ...form, full_name: event.target.value })}
          />
        </label>

        <label>
          {t.email}
          <input
            type="email"
            value={form.email}
            onChange={(event) => setForm({ ...form, email: event.target.value })}
          />
        </label>

        <label>
          {t.password}
          <input
            type="password"
            value={form.password}
            onChange={(event) => setForm({ ...form, password: event.target.value })}
          />
        </label>

        <label>
          {t.companyName}
          <input
            value={form.company_name}
            onChange={(event) =>
              setForm({ ...form, company_name: event.target.value })
            }
          />
        </label>

        <label>
          {t.userRole}
          <select
            value={form.role}
            onChange={(event) => setForm({ ...form, role: event.target.value })}
          >
            <option value="customer">customer</option>
            <option value="admin">admin</option>
            <option value="sales_manager">sales_manager</option>
            <option value="operations_staff">operations_staff</option>
            <option value="product_manager">product_manager</option>
            <option value="super_admin">super_admin</option>
          </select>
        </label>

        <button className="primary-button" type="button" onClick={createInternalUser}>
          {t.createInternalUser}
        </button>
      </div>
    </ToolPage>
  );
}

function DashboardPage({ t, user, language }) {
  const base = getBase(language);
  const isAdmin = user && ["admin", "super_admin"].includes(user.role);

  return (
    <section className="detail-page">
      <p className="section-label">{t.dashboardTitle}</p>
      <h2>{user ? user.full_name : t.notLoggedIn}</h2>

      {user && (
        <div className="user-card">
          <p>
            <strong>{t.email}:</strong> {user.email}
          </p>
          <p>
            <strong>{t.role}:</strong> {user.role}
          </p>
        </div>
      )}

      <div className="dashboard-grid">
        <a className="feature-card" href={`${base}/products`}>
          <h3>{t.publicTools}</h3>
          <p>GET /products/</p>
        </a>

        <a className="feature-card" href={`${base}/quotes`}>
          <h3>{t.customerTools}</h3>
          <p>POST /quotes/ - GET /quotes/my</p>
        </a>

        <a className="feature-card" href={`${base}/orders`}>
          <h3>{t.nav.orders}</h3>
          <p>GET /orders/my</p>
        </a>

        {isAdmin && (
          <a className="feature-card" href={`${base}/admin`}>
            <h3>{t.adminTools}</h3>
            <p>Products, quotes, orders, users</p>
          </a>
        )}
      </div>
    </section>
  );
}

function ApiPage({ t }) {
  return (
    <ToolPage title={t.endpointPanel}>
      <a className="endpoint-link" href={`${API_BASE}/`}>
        <strong>GET /</strong>
        <span>Root endpoint</span>
      </a>

      <a className="endpoint-link" href={`${API_BASE}/docs`}>
        <strong>Swagger Docs</strong>
        <span>Interactive API docs</span>
      </a>

      <a className="endpoint-link" href={`${API_BASE}/openapi.json`}>
        <strong>OpenAPI JSON</strong>
        <span>Raw API schema</span>
      </a>
    </ToolPage>
  );
}

function ToolPage({ title, children }) {
  return (
    <section className="detail-page">
      <p className="section-label">RePG API</p>
      <h2>{title}</h2>
      <div className="tool-grid">{children}</div>
    </section>
  );
}

function FormShell({ title, children }) {
  return (
    <section className="detail-page">
      <p className="section-label">RePG Portal</p>
      <h2>{title}</h2>
      {children}
    </section>
  );
}

function ActionButton({ label, text, onClick }) {
  return (
    <button className="endpoint-link button-link" type="button" onClick={onClick}>
      <strong>{label}</strong>
      <span>{text}</span>
    </button>
  );
}

function OutputPanel({ t, output }) {
  return (
    <section className="output-panel">
      <h3>{t.response}</h3>
      <pre>{typeof output === "string" ? output : JSON.stringify(output, null, 2)}</pre>
    </section>
  );
}

function App() {
  const [path, setPath] = useState(window.location.pathname);
  const [token, setToken] = useState(localStorage.getItem("repg_token") || "");
  const [user, setUser] = useState(null);
  const [output, setOutput] = useState(null);

  const language = getLanguage();
  const page = getPage();
  const t = text[language];

  const currentUserLabel = useMemo(() => {
    if (!user) {
      return t.notLoggedIn;
    }

    return `${user.full_name} - ${user.role}`;
  }, [t.notLoggedIn, user]);

  useEffect(() => {
    function updatePath() {
      setPath(window.location.pathname);
    }

    window.addEventListener("popstate", updatePath);
    return () => window.removeEventListener("popstate", updatePath);
  }, []);

  useEffect(() => {
    if (!token) {
      return;
    }

    apiRequest("/auth/me", {}, token)
      .then((data) => {
        setUser(data);
      })
      .catch(() => {
        localStorage.removeItem("repg_token");
        setToken("");
        setUser(null);
      });
  }, [token, path]);

  function handleLogin(nextToken, nextUser) {
    setToken(nextToken);
    setUser(nextUser);
  }

  function handleLogout() {
    localStorage.removeItem("repg_token");
    setToken("");
    setUser(null);
    setOutput(null);
  }

  let pageContent = <HomePage language={language} t={t} />;

  if (page === "login") {
    pageContent = (
      <LoginPage
        language={language}
        t={t}
        onLogin={handleLogin}
        setOutput={setOutput}
      />
    );
  }

  if (page === "register") {
    pageContent = <RegisterPage t={t} setOutput={setOutput} />;
  }

  if (page === "dashboard") {
    pageContent = <DashboardPage language={language} t={t} user={user} />;
  }

  if (page === "products") {
    pageContent = <ProductsPage t={t} token={token} setOutput={setOutput} />;
  }

  if (page === "quotes") {
    pageContent = <QuotesPage t={t} token={token} setOutput={setOutput} />;
  }

  if (page === "orders") {
    pageContent = <OrdersPage t={t} token={token} setOutput={setOutput} />;
  }

  if (page === "admin") {
    pageContent = <AdminPage t={t} token={token} setOutput={setOutput} />;
  }

  if (page === "api") {
    pageContent = <ApiPage t={t} />;
  }

  return (
    <main className="page-shell">
      <Header language={language} t={t} user={user} onLogout={handleLogout} />

      <div className="status-strip">
        <span>{t.currentUser}: {currentUserLabel}</span>
      </div>

      {pageContent}

      {output && <OutputPanel t={t} output={output} />}

      <footer className="site-footer">
        <p>{t.portal}</p>
        <div>
          <a href={`${getBase(language)}/login`}>{t.nav.login}</a>
          <a href={`${getBase(language)}/register`}>{t.nav.register}</a>
          <a href={`${API_BASE}/docs`}>Swagger</a>
        </div>
      </footer>
    </main>
  );
}

export default App;