import "./App.css";

const API_BASE = "https://api.ayartuerk.me";

const translations = {
  en: {
    language: "EN",
    otherLanguage: "TR",
    otherPath: "/tr/",
    nav: {
      home: "Home",
      products: "Products",
      quotes: "Quotes",
      orders: "Orders",
      admin: "Admin",
      api: "API",
    },
    heroTitle: "Clean technology product and quote management portal.",
    heroText:
      "A RePG-style frontend for product browsing, quote requests, order tracking, and admin workflows powered by the FastAPI backend.",
    primaryCta: "Browse Products",
    secondaryCta: "Open API Docs",
    statusTitle: "Live Backend",
    statusItems: ["FastAPI", "PostgreSQL", "JWT Auth", "Quote Workflow"],
    introTitle: "Built around renewable energy and water technology workflows.",
    introText:
      "The interface follows a clean corporate layout inspired by RePG's energy and water technology positioning, while exposing the backend project's product, quote, order, and admin capabilities.",
    cards: [
      {
        title: "Product Catalogue",
        text: "Public users can browse products and inspect product details.",
        link: "/en/products",
      },
      {
        title: "Quote Workflow",
        text: "Authenticated users can create quote requests and view their quote history.",
        link: "/en/quotes",
      },
      {
        title: "Order Tracking",
        text: "Users can view orders created from approved quotes.",
        link: "/en/orders",
      },
      {
        title: "Admin Controls",
        text: "Admins can manage products, quote status, order creation, and internal users.",
        link: "/en/admin",
      },
    ],
    pages: {
      products: {
        title: "Products",
        text: "Use this page for product catalogue browsing and product detail access.",
        actions: [
          ["GET /products/", "List public products", `${API_BASE}/docs#/products`],
          ["GET /products/{product_id}", "View one product", `${API_BASE}/docs#/products`],
        ],
      },
      login: {
        title: "Login",
        text: "Use this page later for JWT login and token storage.",
        actions: [
          ["POST /auth/login", "Login and receive access token", `${API_BASE}/docs#/auth`],
          ["GET /auth/me", "Check current authenticated user", `${API_BASE}/docs#/auth`],
        ],
      },
      register: {
        title: "Register",
        text: "Use this page later for public customer registration.",
        actions: [
          ["POST /users/", "Create public user account", `${API_BASE}/docs#/users`],
        ],
      },
      quotes: {
        title: "Quotes",
        text: "Use this page later for quote creation and quote history.",
        actions: [
          ["POST /quotes/", "Create quote request", `${API_BASE}/docs#/quotes`],
          ["GET /quotes/my", "View my quotes", `${API_BASE}/docs#/quotes`],
          ["GET /quotes/{quote_id}", "View one quote", `${API_BASE}/docs#/quotes`],
        ],
      },
      orders: {
        title: "Orders",
        text: "Use this page later for order history and order detail views.",
        actions: [
          ["GET /orders/my", "View my orders", `${API_BASE}/docs#/orders`],
          ["GET /orders/{order_id}", "View one order", `${API_BASE}/docs#/orders`],
        ],
      },
      admin: {
        title: "Admin Dashboard",
        text: "Use this page later for admin-only product, quote, order, and user controls.",
        actions: [
          ["POST /products/", "Create product", `${API_BASE}/docs#/products`],
          ["PUT /products/{product_id}", "Update product", `${API_BASE}/docs#/products`],
          ["DELETE /products/{product_id}", "Delete product", `${API_BASE}/docs#/products`],
          ["GET /quotes/", "List all quotes", `${API_BASE}/docs#/quotes`],
          ["PATCH /quotes/{quote_id}/status", "Approve or reject quote", `${API_BASE}/docs#/quotes`],
          ["POST /orders/from-quote/{quote_id}", "Create order from quote", `${API_BASE}/docs#/orders`],
          ["GET /orders/", "List all orders", `${API_BASE}/docs#/orders`],
          ["POST /admin/users/", "Create internal admin user", `${API_BASE}/docs#/admin-users`],
        ],
      },
      api: {
        title: "API Endpoint Access",
        text: "Direct access panel for the backend endpoints currently exposed by the project.",
        actions: [
          ["GET /", "Root health endpoint", `${API_BASE}/`],
          ["Swagger Docs", "Interactive OpenAPI documentation", `${API_BASE}/docs`],
          ["OpenAPI JSON", "Raw OpenAPI schema", `${API_BASE}/openapi.json`],
        ],
      },
    },
    footer: "Frontend prototype for RePG Product & Quote Management API.",
  },
  tr: {
    language: "TR",
    otherLanguage: "EN",
    otherPath: "/en/",
    nav: {
      home: "Ana Sayfa",
      products: "Ürünler",
      quotes: "Teklifler",
      orders: "Siparişler",
      admin: "Admin",
      api: "API",
    },
    heroTitle: "Temiz teknoloji ürün ve teklif yönetim portalı.",
    heroText:
      "FastAPI backend tarafından desteklenen ürün görüntüleme, teklif talepleri, sipariş takibi ve admin iş akışları için RePG tarzı frontend.",
    primaryCta: "Ürünleri İncele",
    secondaryCta: "API Dokümantasyonu",
    statusTitle: "Canlı Backend",
    statusItems: ["FastAPI", "PostgreSQL", "JWT Auth", "Teklif İş Akışı"],
    introTitle: "Yenilenebilir enerji ve su teknolojisi iş akışları etrafında kuruldu.",
    introText:
      "Arayüz, RePG'nin enerji ve su teknolojisi konumlandırmasından ilham alan temiz kurumsal bir düzen izlerken backend projesinin ürün, teklif, sipariş ve admin yeteneklerini sunar.",
    cards: [
      {
        title: "Ürün Kataloğu",
        text: "Public kullanıcılar ürünleri görüntüleyebilir ve ürün detaylarını inceleyebilir.",
        link: "/tr/products",
      },
      {
        title: "Teklif İş Akışı",
        text: "Giriş yapan kullanıcılar teklif talebi oluşturabilir ve teklif geçmişini görebilir.",
        link: "/tr/quotes",
      },
      {
        title: "Sipariş Takibi",
        text: "Kullanıcılar onaylanmış tekliflerden oluşturulan siparişleri görüntüleyebilir.",
        link: "/tr/orders",
      },
      {
        title: "Admin Kontrolleri",
        text: "Adminler ürünleri, teklif durumlarını, sipariş oluşturmayı ve iç kullanıcıları yönetebilir.",
        link: "/tr/admin",
      },
    ],
    pages: {
      products: {
        title: "Ürünler",
        text: "Bu sayfa ürün kataloğu ve ürün detay erişimi için kullanılacak.",
        actions: [
          ["GET /products/", "Public ürünleri listele", `${API_BASE}/docs#/products`],
          ["GET /products/{product_id}", "Tek ürünü görüntüle", `${API_BASE}/docs#/products`],
        ],
      },
      login: {
        title: "Giriş",
        text: "Bu sayfa daha sonra JWT login ve token saklama için kullanılacak.",
        actions: [
          ["POST /auth/login", "Giriş yap ve access token al", `${API_BASE}/docs#/auth`],
          ["GET /auth/me", "Mevcut kullanıcıyı kontrol et", `${API_BASE}/docs#/auth`],
        ],
      },
      register: {
        title: "Kayıt",
        text: "Bu sayfa daha sonra public müşteri kaydı için kullanılacak.",
        actions: [
          ["POST /users/", "Public kullanıcı hesabı oluştur", `${API_BASE}/docs#/users`],
        ],
      },
      quotes: {
        title: "Teklifler",
        text: "Bu sayfa daha sonra teklif oluşturma ve teklif geçmişi için kullanılacak.",
        actions: [
          ["POST /quotes/", "Teklif talebi oluştur", `${API_BASE}/docs#/quotes`],
          ["GET /quotes/my", "Tekliflerimi görüntüle", `${API_BASE}/docs#/quotes`],
          ["GET /quotes/{quote_id}", "Tek teklifi görüntüle", `${API_BASE}/docs#/quotes`],
        ],
      },
      orders: {
        title: "Siparişler",
        text: "Bu sayfa daha sonra sipariş geçmişi ve sipariş detayları için kullanılacak.",
        actions: [
          ["GET /orders/my", "Siparişlerimi görüntüle", `${API_BASE}/docs#/orders`],
          ["GET /orders/{order_id}", "Tek siparişi görüntüle", `${API_BASE}/docs#/orders`],
        ],
      },
      admin: {
        title: "Admin Paneli",
        text: "Bu sayfa daha sonra admin-only ürün, teklif, sipariş ve kullanıcı kontrolleri için kullanılacak.",
        actions: [
          ["POST /products/", "Ürün oluştur", `${API_BASE}/docs#/products`],
          ["PUT /products/{product_id}", "Ürün güncelle", `${API_BASE}/docs#/products`],
          ["DELETE /products/{product_id}", "Ürün sil", `${API_BASE}/docs#/products`],
          ["GET /quotes/", "Tüm teklifleri listele", `${API_BASE}/docs#/quotes`],
          ["PATCH /quotes/{quote_id}/status", "Teklifi onayla veya reddet", `${API_BASE}/docs#/quotes`],
          ["POST /orders/from-quote/{quote_id}", "Tekliften sipariş oluştur", `${API_BASE}/docs#/orders`],
          ["GET /orders/", "Tüm siparişleri listele", `${API_BASE}/docs#/orders`],
          ["POST /admin/users/", "İç admin kullanıcısı oluştur", `${API_BASE}/docs#/admin-users`],
        ],
      },
      api: {
        title: "API Endpoint Erişimi",
        text: "Projede mevcut backend endpointleri için doğrudan erişim paneli.",
        actions: [
          ["GET /", "Root health endpoint", `${API_BASE}/`],
          ["Swagger Docs", "Interactive OpenAPI dokümantasyonu", `${API_BASE}/docs`],
          ["OpenAPI JSON", "Raw OpenAPI şeması", `${API_BASE}/openapi.json`],
        ],
      },
    },
    footer: "RePG Product & Quote Management API için frontend prototipi.",
  },
};

function getLanguage() {
  return window.location.pathname.startsWith("/tr") ? "tr" : "en";
}

function getPage() {
  const parts = window.location.pathname.split("/").filter(Boolean);
  return parts[1] || "home";
}

function HomePage({ t }) {
  return (
    <>
      <section className="hero-section">
        <div className="hero-content">
          <p className="section-label">RePG Portal</p>
          <h2>{t.heroTitle}</h2>
          <p className="hero-text">{t.heroText}</p>

          <div className="hero-actions">
            <a className="primary-button" href={`/${t.language.toLowerCase()}/products`}>
              {t.primaryCta}
            </a>
            <a className="secondary-button" href={`${API_BASE}/docs`}>
              {t.secondaryCta}
            </a>
          </div>
        </div>

        <aside className="hero-card">
          <p>{t.statusTitle}</p>
          <h3>api.ayartuerk.me</h3>
          {t.statusItems.map((item) => (
            <span key={item}>{item}</span>
          ))}
        </aside>
      </section>

      <section className="intro-section">
        <p className="section-label">Clean Technology</p>
        <h2>{t.introTitle}</h2>
        <p>{t.introText}</p>
      </section>

      <section className="card-grid-section">
        {t.cards.map((card) => (
          <a className="feature-card" href={card.link} key={card.title}>
            <h3>{card.title}</h3>
            <p>{card.text}</p>
            <span>Open →</span>
          </a>
        ))}
      </section>

      <section className="endpoint-panel">
        <div>
          <p className="section-label">API</p>
          <h2>{t.pages.api.title}</h2>
          <p>{t.pages.api.text}</p>
        </div>

        <div className="endpoint-list">
          {t.pages.api.actions.map(([method, text, link]) => (
            <a href={link} key={method}>
              <strong>{method}</strong>
              <span>{text}</span>
            </a>
          ))}
        </div>
      </section>
    </>
  );
}

function DetailPage({ page, t }) {
  const data = t.pages[page] || t.pages.api;

  return (
    <section className="detail-page">
      <p className="section-label">RePG Portal</p>
      <h2>{data.title}</h2>
      <p>{data.text}</p>

      <div className="endpoint-list large">
        {data.actions.map(([method, text, link]) => (
          <a href={link} key={`${method}-${text}`}>
            <strong>{method}</strong>
            <span>{text}</span>
          </a>
        ))}
      </div>
    </section>
  );
}

function App() {
  const language = getLanguage();
  const page = getPage();
  const t = translations[language];
  const base = `/${language}`;

  return (
    <main className="page-shell">
      <header className="site-header">
        <a className="brand" href={`${base}/`}>
          <div className="brand-mark">RePG</div>
          <div>
            <p className="brand-kicker">Renewable Energy Power Generation</p>
            <h1>Product & Quote Portal</h1>
          </div>
        </a>

        <nav className="nav-links" aria-label="Main navigation">
          <a href={`${base}/`}>{t.nav.home}</a>
          <a href={`${base}/products`}>{t.nav.products}</a>
          <a href={`${base}/quotes`}>{t.nav.quotes}</a>
          <a href={`${base}/orders`}>{t.nav.orders}</a>
          <a href={`${base}/admin`}>{t.nav.admin}</a>
          <a href={`${base}/api`}>{t.nav.api}</a>
          <a className="language-switch" href={t.otherPath}>
            {t.otherLanguage}
          </a>
        </nav>
      </header>

      {page === "home" ? <HomePage t={t} /> : <DetailPage page={page} t={t} />}

      <footer className="site-footer">
        <p>{t.footer}</p>
        <div>
          <a href={`${base}/login`}>Login</a>
          <a href={`${base}/register`}>Register</a>
          <a href={`${API_BASE}/docs`}>Swagger</a>
        </div>
      </footer>
    </main>
  );
}

export default App;