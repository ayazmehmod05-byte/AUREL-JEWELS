const fs = require('fs');
const path = require('path');

const pages = [
  { file: 'rings.html', label: 'Rings', icon: 'fa-ring' },
  { file: 'earrings.html', label: 'Earrings', icon: 'fa-ear-listen' },
  { file: 'necklaces.html', label: 'Necklaces', icon: 'fa-link' },
  { file: 'pendants.html', label: 'Pendants', icon: 'fa-gem' },
  { file: 'bracelets.html', label: 'Bracelets', icon: 'fa-circle-notch' },
  { file: 'bangles.html', label: 'Bangles', icon: 'fa-circle' },
];

function navFor(activeFile) {
  const itemMarkup = pages.map((page, index) => {
    const divider = index === 4 ? '        <div class="dropdown-divider"></div>\n' : '';
    const active = page.file === activeFile ? ' active-page' : '';
    return `${divider}        <a href="${page.file}" class="dropdown-item${active}" role="menuitem">
          <i class="fa-solid ${page.icon}"></i> ${page.label}
        </a>`;
  }).join('\n');

  return `<nav id="navbar">
  <a href="store.html" class="logo">AUREL <span>JEWELS</span></a>
  <ul class="nav-links">
    <li><a href="store.html#home">Home</a></li>
    <li><a href="store.html#smart-ring">Smart Wearables</a></li>
    <li><a href="store.html#shop">Curations</a></li>
    <li class="nav-dropdown" id="collections-dropdown">
      <button class="nav-dropdown-trigger" id="collectionsBtn" aria-expanded="false" aria-haspopup="true">
        Collections
        <i class="fa-solid fa-chevron-down" aria-hidden="true"></i>
      </button>
      <div class="nav-dropdown-menu" id="collectionsMenu" role="menu">
${itemMarkup}
      </div>
    </li>
    <li><a href="store.html#stack-builder">Styling Guide</a></li>
    <li><a href="store.html#about">Our Brand</a></li>
    <li><a href="store.html#contact">Contact</a></li>
  </ul>
  <div class="nav-actions">
    <a href="store.html#contact" class="cta-btn">Custom Inquiry</a>
  </div>
</nav>`;
}

const overrides = String.raw`
<style id="collection-uniform-overrides">
  :root {
    --gold: #D4AF37;
    --gold-light: #e8cc6a;
    --gold-dark: #a88a1e;
    --dark: #0f0f11;
    --dark-2: #16161a;
    --white: #ffffff;
    --gray: #7a7a85;
    --radius: 14px;
    --font-serif: 'Playfair Display', Georgia, serif;
    --font-sans: 'Outfit', 'Inter', Arial, sans-serif;
  }

  html,
  body {
    background: #0f0f11 !important;
    color: #ffffff !important;
    overflow-x: hidden !important;
  }

  body {
    font-family: var(--font-sans) !important;
    line-height: 1.6 !important;
  }

  body::before,
  body::after,
  .hero-orb,
  .hero-particle,
  .hero-deco,
  .hero-deco-ring,
  .hero-ring,
  .hero-shimmer,
  .hero-pattern,
  .hero-stats,
  .category-strip,
  .filter-bar,
  .upload-note,
  .bespoke-cta {
    display: none !important;
  }

  #navbar {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    width: 100% !important;
    min-height: 76px !important;
    padding: 1.55rem 5% !important;
    background: rgba(255, 255, 255, 0.85) !important;
    backdrop-filter: blur(25px) !important;
    -webkit-backdrop-filter: blur(25px) !important;
    z-index: 1000 !important;
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    gap: 1.5rem !important;
    border-bottom: 1px solid rgba(212, 175, 55, 0.12) !important;
    box-shadow: none !important;
    transition: all 0.35s ease !important;
  }

  #navbar.scrolled {
    padding: 1.05rem 5% !important;
    background: rgba(255, 255, 255, 0.96) !important;
    border-bottom-color: rgba(212, 175, 55, 0.3) !important;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.08) !important;
  }

  #navbar .logo {
    font-family: var(--font-serif) !important;
    font-size: clamp(1.45rem, 3vw, 2.15rem) !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    color: #000000 !important;
    text-decoration: none !important;
    white-space: nowrap !important;
  }

  #navbar .logo span {
    color: var(--gold) !important;
  }

  #navbar .nav-links {
    display: flex !important;
    gap: clamp(0.8rem, 1.7vw, 2.6rem) !important;
    list-style: none !important;
    align-items: center !important;
    margin: 0 !important;
    padding: 0 !important;
  }

  #navbar .nav-links > li {
    position: relative !important;
    display: flex !important;
    align-items: center !important;
  }

  #navbar .nav-links a,
  #navbar .nav-dropdown-trigger {
    text-decoration: none !important;
    color: #000000 !important;
    font-family: var(--font-sans) !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    letter-spacing: 1.8px !important;
    text-transform: uppercase !important;
    position: relative !important;
    transition: color 0.3s ease !important;
    background: none !important;
    border: 0 !important;
    padding: 0 !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.35rem !important;
    border-radius: 0 !important;
    white-space: nowrap !important;
  }

  #navbar .nav-links > li > a::after,
  #navbar .nav-dropdown-trigger::after {
    content: '' !important;
    position: absolute !important;
    bottom: -6px !important;
    left: 0 !important;
    width: 0 !important;
    height: 1.5px !important;
    background: var(--gold) !important;
    transition: width 0.35s ease !important;
  }

  #navbar .nav-links > li > a:hover::after,
  #navbar .nav-dropdown:hover .nav-dropdown-trigger::after,
  #navbar .nav-dropdown.open .nav-dropdown-trigger::after,
  #navbar .nav-dropdown-trigger.open::after {
    width: 100% !important;
  }

  #navbar .nav-dropdown-trigger i {
    font-size: 0.7rem !important;
    color: var(--gold) !important;
    transition: transform 0.3s ease !important;
  }

  #navbar .nav-dropdown:hover .nav-dropdown-trigger i,
  #navbar .nav-dropdown.open .nav-dropdown-trigger i,
  #navbar .nav-dropdown-trigger.open i {
    transform: rotate(180deg) !important;
  }

  #navbar .nav-dropdown-menu {
    position: absolute !important;
    top: calc(100% + 18px) !important;
    left: 50% !important;
    min-width: 200px !important;
    padding: 0.6rem 0 !important;
    background: rgba(255, 255, 255, 0.92) !important;
    border: 1px solid rgba(201, 169, 97, 0.4) !important;
    border-radius: 12px !important;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.1) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    opacity: 0 !important;
    visibility: hidden !important;
    pointer-events: none !important;
    transform: translateX(-50%) translateY(-8px) !important;
    transition: opacity 0.3s ease, transform 0.3s ease, visibility 0.3s ease !important;
    z-index: 1001 !important;
  }

  #navbar .nav-dropdown:hover .nav-dropdown-menu,
  #navbar .nav-dropdown.open .nav-dropdown-menu,
  #navbar .nav-dropdown-menu.open {
    opacity: 1 !important;
    visibility: visible !important;
    pointer-events: auto !important;
    transform: translateX(-50%) translateY(0) !important;
  }

  #navbar .nav-dropdown-menu::before {
    content: '' !important;
    position: absolute !important;
    top: -6px !important;
    left: 50% !important;
    width: 12px !important;
    height: 12px !important;
    background: rgba(255, 255, 255, 0.92) !important;
    border-left: 1px solid rgba(201, 169, 97, 0.4) !important;
    border-top: 1px solid rgba(201, 169, 97, 0.4) !important;
    transform: translateX(-50%) rotate(45deg) !important;
  }

  #navbar .dropdown-item {
    display: flex !important;
    align-items: center !important;
    gap: 0.75rem !important;
    padding: 0.75rem 1.4rem !important;
    color: #000000 !important;
    font-size: 0.82rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
    border-left: 2px solid transparent !important;
    transition: all 0.2s ease !important;
    border-radius: 0 !important;
  }

  #navbar .dropdown-item i {
    width: 20px !important;
    text-align: center !important;
    color: var(--gold) !important;
  }

  #navbar .dropdown-item:hover,
  #navbar .dropdown-item.active-page,
  #navbar .dropdown-item.active {
    color: var(--gold) !important;
    background: rgba(212, 175, 55, 0.06) !important;
    border-left-color: var(--gold) !important;
    padding-left: 1.7rem !important;
  }

  #navbar .dropdown-divider {
    height: 1px !important;
    background: rgba(212, 175, 55, 0.16) !important;
    margin: 0.35rem 1.1rem !important;
  }

  #navbar .nav-actions {
    display: flex !important;
    align-items: center !important;
  }

  #navbar .cta-btn {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 0.85rem 1.35rem !important;
    background: linear-gradient(135deg, var(--gold), var(--gold-light)) !important;
    color: #000000 !important;
    border: 1px solid rgba(212, 175, 55, 0.55) !important;
    border-radius: 4px !important;
    font-family: var(--font-sans) !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 1.3px !important;
    text-transform: uppercase !important;
    text-decoration: none !important;
    white-space: nowrap !important;
    box-shadow: 0 10px 22px rgba(212, 175, 55, 0.18) !important;
  }

  .hero-spacer {
    display: none !important;
  }

  .category-hero,
  .page-hero {
    height: 380px !important;
    min-height: 380px !important;
    margin-top: 76px !important;
    padding: 0 48px !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    background: radial-gradient(circle at 40% 50%, #1a1014 0%, #0f0f11 100%) !important;
    position: relative !important;
    overflow: hidden !important;
  }

  .category-hero::before,
  .page-hero::before {
    content: '' !important;
    position: absolute !important;
    width: 520px !important;
    height: 520px !important;
    border-radius: 50% !important;
    border: 1px solid rgba(212, 175, 55, 0.08) !important;
    top: 50% !important;
    left: 42% !important;
    transform: translate(-50%, -50%) !important;
    pointer-events: none !important;
  }

  .category-hero::after,
  .page-hero::after {
    content: '' !important;
    position: absolute !important;
    width: 320px !important;
    height: 320px !important;
    border-radius: 50% !important;
    border: 1px solid rgba(212, 175, 55, 0.06) !important;
    top: 50% !important;
    left: 42% !important;
    transform: translate(-50%, -50%) !important;
    pointer-events: none !important;
  }

  .category-hero > *,
  .page-hero > *,
  .hero-inner,
  .hero-content {
    position: relative !important;
    z-index: 1 !important;
  }

  .hero-inner,
  .hero-content {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    max-width: 760px !important;
    margin: 0 auto !important;
  }

  .breadcrumb,
  .hero-breadcrumb,
  .page-hero-breadcrumb {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 0.55rem !important;
    margin: 0 0 18px !important;
    padding: 0 !important;
    background: transparent !important;
    color: var(--gray) !important;
    font-family: var(--font-sans) !important;
    font-size: 0.78rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
  }

  .breadcrumb a,
  .hero-breadcrumb a,
  .page-hero-breadcrumb a {
    color: var(--gray) !important;
    text-decoration: none !important;
  }

  .breadcrumb span,
  .breadcrumb .sep,
  .breadcrumb .current,
  .hero-breadcrumb span,
  .hero-breadcrumb .sep,
  .hero-breadcrumb .current,
  .page-hero-breadcrumb span {
    color: var(--gold) !important;
  }

  .hero-accent,
  .hero-line,
  .hero-rule,
  .hero-accent-line,
  .category-hero .hero-inner::before,
  .page-hero .hero-inner::before,
  .category-hero .hero-content::before,
  .page-hero .hero-content::before {
    content: '' !important;
    display: block !important;
    width: 52px !important;
    height: 3px !important;
    min-height: 3px !important;
    background: linear-gradient(90deg, var(--gold), var(--gold-light)) !important;
    border-radius: 2px !important;
    margin: 0 auto 22px !important;
  }

  .hero-label,
  .hero-eyebrow {
    display: none !important;
  }

  .category-hero h1,
  .page-hero h1,
  .hero-title {
    font-family: var(--font-serif) !important;
    font-size: clamp(3rem, 6vw, 4rem) !important;
    font-weight: 700 !important;
    color: var(--gold) !important;
    letter-spacing: 0.02em !important;
    line-height: 1.1 !important;
    margin: 0 0 16px !important;
    text-align: center !important;
  }

  .category-hero h1 span,
  .category-hero h1 em,
  .page-hero h1 span,
  .page-hero h1 em,
  .hero-title span,
  .gold-word {
    color: var(--gold) !important;
    font-style: normal !important;
  }

  .category-hero p,
  .page-hero p,
  .hero-subtitle,
  .page-hero-subtitle {
    max-width: 560px !important;
    color: rgba(255, 255, 255, 0.62) !important;
    font-family: var(--font-sans) !important;
    font-size: 1.02rem !important;
    font-weight: 300 !important;
    line-height: 1.65 !important;
    margin: 0 auto !important;
    text-align: center !important;
  }

  .products-section,
  .shop-section,
  .collection-section,
  .section-wrap {
    width: 100% !important;
    max-width: none !important;
    margin: 0 !important;
    padding: 80px 48px 100px !important;
    background: #0f0f11 !important;
    background-image: none !important;
  }

  .shop-section-inner,
  .section-wrap > .section-header,
  .products-section > .section-header,
  .collection-section > .section-header,
  .shop-section > .sec-title {
    max-width: 1180px !important;
    margin-left: auto !important;
    margin-right: auto !important;
  }

  .section-header,
  .sec-title {
    margin-bottom: 42px !important;
    text-align: left !important;
  }

  .section-label,
  .sec-title span {
    color: var(--gold) !important;
    font-family: var(--font-sans) !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
  }

  .section-title,
  .sec-title h2 {
    color: #ffffff !important;
    font-family: var(--font-serif) !important;
    font-size: clamp(1.8rem, 3vw, 2.25rem) !important;
    font-weight: 600 !important;
    line-height: 1.2 !important;
  }

  .section-count,
  .section-desc,
  .sec-title p {
    color: var(--gray) !important;
  }

  .product-grid {
    display: grid !important;
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
    grid-auto-rows: 1fr !important;
    gap: 28px !important;
    width: 100% !important;
    max-width: 1180px !important;
    margin: 0 auto !important;
    align-items: stretch !important;
  }

  .product-card {
    width: 100% !important;
    min-width: 0 !important;
    min-height: 500px !important;
    height: 100% !important;
    background: #16161a !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: var(--radius) !important;
    overflow: hidden !important;
    box-shadow: none !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: flex-start !important;
    position: relative !important;
    opacity: 1 !important;
    transform: none !important;
    transition: transform 0.35s ease, box-shadow 0.35s ease, border-color 0.35s ease !important;
  }

  .product-card:hover {
    transform: translateY(-7px) !important;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.5), 0 8px 40px rgba(212, 175, 55, 0.18) !important;
    border-color: rgba(212, 175, 55, 0.28) !important;
  }

  .card-image,
  .card-image-wrap,
  .product-img-box {
    width: 100% !important;
    height: 290px !important;
    min-height: 290px !important;
    flex: 0 0 290px !important;
    display: block !important;
    position: relative !important;
    overflow: hidden !important;
    border-radius: 0 !important;
    background: linear-gradient(145deg, #1e1e24, #13131a) !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
  }

  .card-image img,
  .card-image-wrap img,
  .product-img-box img,
  .product-card img {
    width: 100% !important;
    height: 100% !important;
    min-height: 100% !important;
    object-fit: cover !important;
    border-radius: 0 !important;
    display: block !important;
  }

  .card-body,
  .product-info-box {
    flex: 1 1 auto !important;
    min-height: 210px !important;
    padding: 20px 20px 22px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    gap: 0.65rem !important;
    background: transparent !important;
  }

  .product-info-box > div {
    min-width: 0 !important;
  }

  .card-name,
  .product-info-box h3 {
    color: #ffffff !important;
    font-family: var(--font-serif) !important;
    font-size: 1.08rem !important;
    font-weight: 500 !important;
    line-height: 1.35 !important;
    margin: 0 0 0.35rem !important;
    display: -webkit-box !important;
    -webkit-line-clamp: 2 !important;
    -webkit-box-orient: vertical !important;
    overflow: hidden !important;
  }

  .card-price,
  .product-price {
    color: var(--gold) !important;
    font-family: var(--font-sans) !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    margin: 0.35rem 0 0 !important;
  }

  .card-price-sub,
  .product-info-box .desc,
  .product-meta,
  .product-category-badge,
  .product-meta-tag {
    color: var(--gray) !important;
    font-family: var(--font-sans) !important;
    font-size: 0.78rem !important;
    line-height: 1.55 !important;
  }

  .product-info-box .desc {
    display: -webkit-box !important;
    -webkit-line-clamp: 2 !important;
    -webkit-box-orient: vertical !important;
    overflow: hidden !important;
  }

  .product-meta {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 0.35rem !important;
    max-height: 3.2rem !important;
    overflow: hidden !important;
  }

  .product-meta-tag,
  .product-category-badge {
    background: rgba(212, 175, 55, 0.08) !important;
    border: 1px solid rgba(212, 175, 55, 0.16) !important;
    border-radius: 50px !important;
    padding: 0.25rem 0.55rem !important;
    color: rgba(255, 255, 255, 0.7) !important;
  }

  .card-badge,
  .product-badge,
  .gemstone-overlay-tag {
    position: absolute !important;
    top: 14px !important;
    left: 14px !important;
    z-index: 3 !important;
    color: var(--gold) !important;
    background: rgba(15, 15, 17, 0.74) !important;
    border: 1px solid rgba(212, 175, 55, 0.22) !important;
    border-radius: 50px !important;
    padding: 4px 10px !important;
    font-size: 0.65rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
  }

  .gemstone-overlay-tag {
    left: auto !important;
    right: 14px !important;
  }

  .quick-add-overlay {
    position: static !important;
    opacity: 1 !important;
    visibility: visible !important;
    transform: none !important;
    background: transparent !important;
    padding: 0 !important;
  }

  .quick-add-btn,
  .view-btn,
  .card-quick-view {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
    margin-top: auto !important;
    padding: 0.8rem 1rem !important;
    color: #0f0f11 !important;
    background: linear-gradient(135deg, var(--gold), var(--gold-light)) !important;
    border: 1px solid rgba(212, 175, 55, 0.75) !important;
    border-radius: 4px !important;
    font-family: var(--font-sans) !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    cursor: pointer !important;
    opacity: 1 !important;
    visibility: visible !important;
    transform: none !important;
  }

  .contact-section {
    background: #0f0f11 !important;
    background-image: none !important;
  }

  .footer {
    background: #0a0a0c !important;
    background-image: none !important;
  }

  @media (max-width: 1100px) {
    #navbar {
      padding-left: 4% !important;
      padding-right: 4% !important;
    }

    #navbar .nav-links {
      gap: 0.9rem !important;
    }

    #navbar .nav-links a,
    #navbar .nav-dropdown-trigger {
      font-size: 0.76rem !important;
      letter-spacing: 1.1px !important;
    }
  }

  @media (max-width: 900px) {
    #navbar .nav-links {
      display: none !important;
    }

    .category-hero,
    .page-hero {
      height: 330px !important;
      min-height: 330px !important;
      padding: 0 24px !important;
    }

    .products-section,
    .shop-section,
    .collection-section,
    .section-wrap {
      padding: 56px 24px 72px !important;
    }

    .product-grid {
      grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    }
  }

  @media (max-width: 640px) {
    #navbar {
      min-height: 68px !important;
      padding: 0.9rem 5% !important;
    }

    #navbar .logo {
      font-size: 1.35rem !important;
    }

    #navbar .cta-btn {
      padding: 0.7rem 0.85rem !important;
      font-size: 0.68rem !important;
      letter-spacing: 0.8px !important;
    }

    .category-hero,
    .page-hero {
      margin-top: 68px !important;
    }

    .product-grid {
      grid-template-columns: 1fr !important;
    }

    .card-image,
    .card-image-wrap,
    .product-img-box {
      height: 260px !important;
      min-height: 260px !important;
      flex-basis: 260px !important;
    }
  }
</style>
`;

for (const page of pages) {
  const filePath = path.join(__dirname, page.file);
  let html = fs.readFileSync(filePath, 'utf8');

  const navRegex = /<nav\b(?=[^>]*\bid=["']navbar["'])[\s\S]*?<\/nav>/i;
  if (!navRegex.test(html)) {
    throw new Error(`Navbar not found in ${page.file}`);
  }
  html = html.replace(navRegex, navFor(page.file));

  const styleRegex = /\s*<style id="collection-uniform-overrides">[\s\S]*?<\/style>\s*/i;
  if (styleRegex.test(html)) {
    html = html.replace(styleRegex, `\n${overrides}\n`);
  } else {
    html = html.replace(/<\/head>/i, `${overrides}\n</head>`);
  }

  fs.writeFileSync(filePath, html, 'utf8');
}

console.log(`Updated ${pages.length} collection pages.`);
