const fs = require('fs');
const path = require('path');

const dir = 'd:/shopify store';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

const ringVideo = 'WhatsApp Video 2026-06-14 at 1.51.38 AM.mp4';
const modelImages = fs.readdirSync(path.join(dir, 'updated store', 'images')).filter(f => f.endsWith('.jpeg'));
// Let's use the first one as the global background
const bgImage = 'updated store/images/' + modelImages[0];

files.forEach(file => {
  let content = fs.readFileSync(path.join(dir, file), 'utf8');

  // Task 1: COLLECTIONS DROPDOWN
  const dropdownRegex = /<div class="nav-dropdown-menu">([\s\S]*?)<\/div>/g;
  content = content.replace(dropdownRegex, `<div class="nav-dropdown-menu">
        <a href="rings.html" class="dropdown-item">
          <span class="dropdown-item-icon fa-solid fa-ring"></span> Rings
        </a>
        <a href="earrings.html" class="dropdown-item">
          <span class="dropdown-item-icon fa-solid fa-ear-listen"></span> Earrings
        </a>
        <a href="necklaces.html" class="dropdown-item">
          <span class="dropdown-item-icon fa-solid fa-link"></span> Necklaces
        </a>
        <a href="pendants.html" class="dropdown-item">
          <span class="dropdown-item-icon fa-solid fa-gem"></span> Pendants
        </a>
        <div class="dropdown-divider"></div>
        <a href="bracelets.html" class="dropdown-item">
          <span class="dropdown-item-icon fa-solid fa-circle-notch"></span> Bracelets
        </a>
        <a href="bangles.html" class="dropdown-item">
          <span class="dropdown-item-icon fa-solid fa-circle"></span> Bangles
        </a>
      </div>`);

  // Remove the CSS that hides icons
  content = content.replace(/\.dropdown-item-icon:not\(\.fa-solid\) \{\s*display: none;\s*\}/g, '');

  // Task 4: HERO/FIRST PAGE
  if (file === 'store.html') {
    // Also remove the "ADD PRODUCT IMAGE" card if it exists
    // Looking at store.html hero section, it has <div class="hero-image-wrapper">
    const heroImageRegex = /<div class="hero-image-wrapper">([\s\S]*?)<\/div>\s*<\/div>/;
    content = content.replace(heroImageRegex, `<div class="hero-image-wrapper">
      <video autoplay loop muted playsinline style="width:100%; max-width:480px; height:500px; object-fit:cover; border-radius:24px; border:1px solid rgba(201,169,97,0.4); box-shadow:0 25px 60px rgba(0,0,0,0.12); z-index:2;">
        <source src="${ringVideo}" type="video/mp4">
      </video>
    </div>`);
  }

  // Task 2 & 5: BACKGROUNDS & THEME
  const globalCSS = `
  <style>
    /* Task 2: BACKGROUNDS */
    body {
      background-image: url('${bgImage}') !important;
      background-attachment: fixed !important;
      background-size: cover !important;
      background-position: center !important;
      position: relative;
    }
    
    /* Transparent overlay */
    body::after {
      content: "";
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(255, 255, 255, 0.65) !important;
      z-index: -999;
      pointer-events: none;
    }

    /* Make sections transparent so the background shows through */
    section, header, footer, main, .hero, .smart-showcase, .engraving-section, .collections-grid, .bg-light, .bg-dark {
      background: transparent !important;
      background-color: transparent !important;
    }

    /* Task 5: THEME - Glass Effect for cards */
    .product-card, .category-card, .contact-card, .engraving-preview-card, .metric-content-box, .collection-card, .item-card, .finish-selection-box {
      background: rgba(255, 255, 255, 0.6) !important;
      backdrop-filter: blur(10px) !important;
      -webkit-backdrop-filter: blur(10px) !important;
      border: 1px solid rgba(255,255,255,0.4) !important;
      box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07) !important;
    }
    
    /* Ensure text is visible and layout correct */
    .smart-showcase h2, .smart-showcase p, .smart-showcase h3, .smart-showcase li, .smart-showcase span {
      color: #1a1a1a !important; /* Force dark text instead of white since background is white */
    }
  </style>
  `;
  if (!content.includes('/* Task 2: BACKGROUNDS */')) {
    content = content.replace('</head>', `${globalCSS}\n</head>`);
  }

  // Task 3: Product Cards (Inside each product card, add that product's relevant model-wearing-jewelry image)
  // Let's replace the src of img inside product cards or just images in the file that match product images
  const imgMap = {
    'rings': modelImages[1],
    'earrings': modelImages[2],
    'necklaces': modelImages[3],
    'pendants': modelImages[4],
    'bracelets': modelImages[5],
    'bangles': modelImages[6],
    'store': modelImages[7]
  };
  
  let pageType = file.replace('.html', '');
  if (imgMap[pageType]) {
    // Replace product images
    content = content.replace(/<img[^>]*class="[^"]*product-img[^"]*"[^>]*src="[^"]*"([^>]*)>/g, `<img class="product-img" src="updated store/images/${imgMap[pageType]}" $1>`);
    // Also cover regular product images if class is slightly different
    content = content.replace(/<img[^>]*src="[^"]*"([^>]*class="[^"]*product[^"]*"[^>]*)>/g, `<img src="updated store/images/${imgMap[pageType]}" $1>`);
  }

  fs.writeFileSync(path.join(dir, file), content, 'utf8');
});
console.log('Done modifying HTML files with refined logic.');
