import "./App.css";

const content = {
  en: {
    nav: {
      home: "Home",
      energy: "Energy Applications",
      products: "Products",
      quote: "Quote",
      contact: "Contact",
    },
    brandKicker: "Renewable Energy Power Generation",
    title: "RePG Product & Quote Portal",
    heroLabel: "New Generation Energy & Water Technology",
    heroTitle:
      "Backend-powered product and quote management for clean technology solutions.",
    heroText:
      "A responsive frontend interface for browsing products, managing quote requests, and presenting RePG-style renewable energy and water technology workflows.",
    explore: "Explore Products",
    requestQuote: "Request Quote",
    systemStatus: "System Status",
    liveApi: "Live API Connected",
    apiOne: "FastAPI Backend",
    apiTwo: "Product Catalogue",
    apiThree: "Quote Management",
    applicationsLabel: "Applications",
    applicationsTitle: "Clean technology areas",
    applicationsText:
      "The interface follows a corporate clean-energy style and presents the backend project as a structured product, quote, and order system.",
    applications: [
      {
        title: "Energy Applications",
        text: "Systems focused on renewable energy, waste heat recovery, heating, cooling, and electricity generation.",
      },
      {
        title: "Air Water Applications",
        text: "Technology concepts connected to humidity, air, water recovery, and sustainable resource use.",
      },
      {
        title: "Industrial Solutions",
        text: "Clean technology solutions for facilities that need efficient, scalable, and future-ready systems.",
      },
    ],
    productLabel: "Products",
    productTitle: "Product and quote workflow",
    productText:
      "This frontend will later connect directly to the backend endpoints for product browsing, customer quote creation, admin approval, and order generation.",
    products: [
      {
        title: "Product Catalogue",
        text: "Browse available RePG product data from the backend API.",
      },
      {
        title: "Quote Requests",
        text: "Customers can request quotes for selected products and quantities.",
      },
      {
        title: "Order Flow",
        text: "Approved quotes can be converted into orders with auditable item snapshots.",
      },
    ],
    quoteLabel: "Quote Portal",
    quoteTitle:
      "Request clean technology products through a structured backend workflow.",
    openDocs: "Open API Docs",
    footerText: "Frontend prototype for desktop and mobile.",
    backTop: "Back to top",
  },
  tr: {
    nav: {
      home: "Ana Sayfa",
      energy: "Enerji Uygulamaları",
      products: "Ürünler",
      quote: "Teklif",
      contact: "İletişim",
    },
    brandKicker: "Yenilenebilir Enerji Güç Üretimi",
    title: "RePG Ürün ve Teklif Portalı",
    heroLabel: "Yeni Nesil Enerji ve Su Teknolojisi",
    heroTitle:
      "Temiz teknoloji çözümleri için backend destekli ürün ve teklif yönetimi.",
    heroText:
      "Ürünleri incelemek, teklif taleplerini yönetmek ve RePG tarzı yenilenebilir enerji ve su teknolojisi iş akışlarını sunmak için responsive frontend arayüzü.",
    explore: "Ürünleri İncele",
    requestQuote: "Teklif İste",
    systemStatus: "Sistem Durumu",
    liveApi: "Canlı API Bağlantısı",
    apiOne: "FastAPI Backend",
    apiTwo: "Ürün Kataloğu",
    apiThree: "Teklif Yönetimi",
    applicationsLabel: "Uygulamalar",
    applicationsTitle: "Temiz teknoloji alanları",
    applicationsText:
      "Arayüz, kurumsal temiz enerji tarzını takip eder ve backend projesini yapılandırılmış ürün, teklif ve sipariş sistemi olarak sunar.",
    applications: [
      {
        title: "Enerji Uygulamaları",
        text: "Yenilenebilir enerji, atık ısı geri kazanımı, ısıtma, soğutma ve elektrik üretimine odaklanan sistemler.",
      },
      {
        title: "Hava Su Uygulamaları",
        text: "Nem, hava, su geri kazanımı ve sürdürülebilir kaynak kullanımı ile bağlantılı teknoloji konseptleri.",
      },
      {
        title: "Endüstriyel Çözümler",
        text: "Verimli, ölçeklenebilir ve geleceğe hazır sistemlere ihtiyaç duyan tesisler için temiz teknoloji çözümleri.",
      },
    ],
    productLabel: "Ürünler",
    productTitle: "Ürün ve teklif iş akışı",
    productText:
      "Bu frontend daha sonra ürün görüntüleme, müşteri teklif oluşturma, admin onayı ve sipariş oluşturma için doğrudan backend endpointlerine bağlanacak.",
    products: [
      {
        title: "Ürün Kataloğu",
        text: "Backend API üzerinden mevcut RePG ürün verilerini inceleyin.",
      },
      {
        title: "Teklif Talepleri",
        text: "Müşteriler seçilen ürünler ve miktarlar için teklif talep edebilir.",
      },
      {
        title: "Sipariş Akışı",
        text: "Onaylanan teklifler, denetlenebilir ürün kopyaları ile siparişlere dönüştürülebilir.",
      },
    ],
    quoteLabel: "Teklif Portalı",
    quoteTitle:
      "Temiz teknoloji ürünlerini yapılandırılmış backend iş akışı üzerinden talep edin.",
    openDocs: "API Dokümantasyonunu Aç",
    footerText: "Masaüstü ve mobil için frontend prototipi.",
    backTop: "Yukarı dön",
  },
};

function getLanguage() {
  const path = window.location.pathname;

  if (path.startsWith("/tr")) {
    return "tr";
  }

  return "en";
}

function App() {
  const language = getLanguage();
  const t = content[language];

  return (
    <main className="page-shell">
      <header className="site-header">
        <div className="brand">
          <div className="brand-mark">RePG</div>
          <div>
            <p className="brand-kicker">{t.brandKicker}</p>
            <h1>{t.title}</h1>
          </div>
        </div>

        <nav className="nav-links" aria-label="Main navigation">
          <a href="#home">{t.nav.home}</a>
          <a href="#applications">{t.nav.energy}</a>
          <a href="#products">{t.nav.products}</a>
          <a href="#quote">{t.nav.quote}</a>
          <a href="#contact">{t.nav.contact}</a>
          <a href="/en/">EN</a>
          <a href="/tr/">TR</a>
        </nav>
      </header>

      <section id="home" className="hero-section">
        <div className="hero-content">
          <p className="section-label">{t.heroLabel}</p>
          <h2>{t.heroTitle}</h2>
          <p className="hero-text">{t.heroText}</p>

          <div className="hero-actions">
            <a className="primary-button" href="#products">
              {t.explore}
            </a>
            <a className="secondary-button" href="#quote">
              {t.requestQuote}
            </a>
          </div>
        </div>

        <div className="hero-card">
          <p>{t.systemStatus}</p>
          <h3>{t.liveApi}</h3>
          <span>{t.apiOne}</span>
          <span>{t.apiTwo}</span>
          <span>{t.apiThree}</span>
        </div>
      </section>

      <section id="applications" className="content-section">
        <div className="section-heading">
          <p className="section-label">{t.applicationsLabel}</p>
          <h2>{t.applicationsTitle}</h2>
          <p>{t.applicationsText}</p>
        </div>

        <div className="card-grid">
          {t.applications.map((item) => (
            <article className="info-card" key={item.title}>
              <h3>{item.title}</h3>
              <p>{item.text}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="products" className="content-section split-section">
        <div>
          <p className="section-label">{t.productLabel}</p>
          <h2>{t.productTitle}</h2>
          <p>{t.productText}</p>
        </div>

        <div className="product-list">
          {t.products.map((item) => (
            <article className="product-card" key={item.title}>
              <h3>{item.title}</h3>
              <p>{item.text}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="quote" className="quote-section">
        <div>
          <p className="section-label">{t.quoteLabel}</p>
          <h2>{t.quoteTitle}</h2>
        </div>
        <a className="primary-button" href="https://api.ayartuerk.me/docs">
          {t.openDocs}
        </a>
      </section>

      <footer id="contact" className="site-footer">
        <div>
          <strong>{t.title}</strong>
          <p>{t.footerText}</p>
        </div>
        <div>
          <a href="https://api.ayartuerk.me/docs">{t.openDocs}</a>
          <a href="#home">{t.backTop}</a>
        </div>
      </footer>
    </main>
  );
}

export default App;