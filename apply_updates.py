"""Apply site-wide updates: spacing, transparent theme, contact sections, grid alignment."""
import re
import glob
import os

DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIR)

COLLECTION_PAGES = [
    'rings.html', 'earrings.html', 'necklaces.html',
    'pendants.html', 'bracelets.html', 'bangles.html'
]

GLOBAL_PATCH_CSS = """
    <style id="site-spacing-theme">
      /* Transparent glass overlay — model backgrounds stay visible */
      section::before, header::before, footer::before, main::before {
        background: rgba(255, 255, 255, 0.42) !important;
      }
      .fixed-model-overlay {
        background: rgba(255, 255, 255, 0.42) !important;
      }
      /* Reduced spacing sitewide */
      .collection-section, .shop-section, .contact-section,
      .smart-showcase, .about-section, .bespoke-cta,
      .engraving-section, .stacking-section, .categories-section {
        padding: 3.5rem 6% !important;
      }
      .contact-section { padding: 3.5rem 6% !important; }
      .sec-title, .section-header { margin-bottom: 2rem !important; }
      .category-hero { height: 300px !important; min-height: 300px !important; }
      .page-hero { padding: 5rem 5% 3rem !important; }
      .section-pad-top { padding-top: 4.5rem !important; }
      .features-strip, .promo-strip, .category-strip { margin: 0 !important; }
      /* Rings-matched product grid for pendants / bracelets / bangles */
      .product-grid {
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 2.5rem !important;
        max-width: none !important;
        margin: 0 !important;
      }
      .product-img-box {
        height: 280px !important;
        aspect-ratio: unset !important;
      }
      .product-img-box img {
        width: 100% !important;
        height: 300px !important;
        object-fit: cover !important;
        border-radius: 12px !important;
        display: block !important;
      }
      .card-image { height: 280px !important; }
      .card-image img {
        width: 100% !important;
        height: 300px !important;
        object-fit: cover !important;
      }
    </style>
"""

CONTACT_CSS = """
    <style id="collection-contact-css">
      .contact-section { padding: 3.5rem 6%; background: transparent; }
      .contact-grid {
        display: grid;
        grid-template-columns: minmax(280px, 0.9fr) minmax(320px, 1.1fr);
        gap: 2.5rem;
        max-width: 1200px;
        margin: 0 auto;
        align-items: stretch;
      }
      .contact-card {
        background: rgba(255,255,255,0.55);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid rgba(201,169,97,0.4);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        display: flex;
        flex-direction: column;
        gap: 1.4rem;
      }
      .contact-method {
        display: grid;
        grid-template-columns: 56px 1fr;
        gap: 1rem;
        align-items: start;
        padding-bottom: 1.4rem;
        border-bottom: 1px solid rgba(201,169,97,0.25);
      }
      .contact-method:last-child { border-bottom: 0; padding-bottom: 0; }
      .contact-icon {
        width: 56px; height: 56px; border-radius: 50%;
        display: grid; place-items: center;
        background: rgba(255,255,255,0.72);
        border: 1px solid rgba(201,169,97,0.4);
      }
      .contact-icon img { width: 30px; height: 30px; object-fit: contain; }
      .contact-card h3 { font-family: 'Playfair Display', serif; font-size: 1.35rem; margin-bottom: 0.5rem; }
      .contact-card p { font-size: 0.9rem; color: #7a7a85; margin-bottom: 0.75rem; }
      .contact-number { font-weight: 700; margin-bottom: 0.75rem; }
      .contact-card-btn {
        display: inline-flex; align-items: center; justify-content: center;
        padding: 0.7rem 1.2rem; background: #0f0f11; color: #fff;
        border-radius: 4px; font-weight: 600; font-size: 0.8rem;
        letter-spacing: 1px; text-transform: uppercase; text-decoration: none;
        transition: background 0.3s;
      }
      .contact-card-btn:hover { background: #D4AF37; color: #0f0f11; }
      .contact-form-card {
        background: rgba(255,255,255,0.55);
        padding: 2rem; border-radius: 16px;
        border: 1px solid rgba(201,169,97,0.4);
        backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
      }
      .contact-form-card h3 { font-family: 'Playfair Display', serif; font-size: 1.45rem; margin-bottom: 1rem; }
      .contact-form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
      .contact-form-card .form-group { margin-bottom: 1rem; }
      .contact-form-card .form-group.full { grid-column: 1 / -1; }
      .contact-form-card label {
        display: block; font-size: 0.75rem; font-weight: 600;
        letter-spacing: 1px; text-transform: uppercase; margin-bottom: 0.4rem;
      }
      .contact-form-card input, .contact-form-card textarea {
        width: 100%; padding: 0.75rem 1rem;
        border: 1px solid rgba(201,169,97,0.35);
        border-radius: 8px; background: rgba(255,255,255,0.8);
        font-family: inherit; font-size: 0.9rem;
      }
      .btn-gold-fill, .contact-submit-btn {
        padding: 0.85rem 2rem; background: #D4AF37; color: #0f0f11;
        border: 1px solid #D4AF37; border-radius: 4px;
        font-weight: 700; font-size: 0.85rem; letter-spacing: 1.5px;
        text-transform: uppercase; cursor: pointer; transition: all 0.3s;
      }
      .btn-gold-fill:hover, .contact-submit-btn:hover {
        background: #e8cb6a; transform: translateY(-2px);
      }
      @media (max-width: 900px) {
        .contact-grid { grid-template-columns: 1fr; }
        .contact-form-grid { grid-template-columns: 1fr; }
      }
    </style>
"""

CONTACT_HTML = """
<!-- CONTACT SECTION -->
<section class="contact-section reveal" id="contact" style="background-image: url('updated store/images/WhatsApp Image 2026-06-14 at 1.10.31 AM (1).jpeg');">
  <div class="sec-title reveal">
    <span>Direct Assistance</span>
    <h2>We're One Message Away</h2>
    <p>Quick questions on sizes, product quality, or order tracking? Contact us instantly.</p>
  </div>
  <div class="contact-grid">
    <div class="contact-card reveal">
      <div class="contact-method">
        <div class="contact-icon"><img src="images/png whatsapp logo.png" alt="WhatsApp"></div>
        <div>
          <h3>WhatsApp Chat Support</h3>
          <p>Quick sizing help, order updates, and product questions.</p>
          <div class="contact-number">0329 6430927</div>
          <a href="https://wa.me/923296430927" target="_blank" class="contact-card-btn">Open WhatsApp</a>
        </div>
      </div>
      <div class="contact-method">
        <div class="contact-icon"><img src="images/gmail png logo.png" alt="Email"></div>
        <div>
          <h3>Email Consultation</h3>
          <p>Custom orders, wholesale requests, and detailed inquiries.</p>
          <div class="contact-number">ayazmehmod05@gmail.com</div>
          <a href="mailto:ayazmehmod05@gmail.com" class="contact-card-btn">Send Email</a>
        </div>
      </div>
    </div>
    <form class="contact-form-card reveal" onsubmit="handleContactSubmit(event)">
      <h3>Send Your Details</h3>
      <div class="contact-form-grid">
        <div class="form-group">
          <label for="contact-full-name">Full Name</label>
          <input type="text" id="contact-full-name" name="full-name" required>
        </div>
        <div class="form-group">
          <label for="contact-email">Email Address</label>
          <input type="email" id="contact-email" name="email" required>
        </div>
        <div class="form-group">
          <label for="contact-phone">Phone Number</label>
          <input type="tel" id="contact-phone" name="phone" required>
        </div>
        <div class="form-group">
          <label for="contact-address">Delivery Address</label>
          <input type="text" id="contact-address" name="delivery-address" required>
        </div>
        <div class="form-group full">
          <label for="contact-message">Your Message</label>
          <textarea id="contact-message" name="message" rows="5" required></textarea>
        </div>
      </div>
      <button type="submit" class="contact-submit-btn">Submit Message</button>
    </form>
  </div>
</section>
"""

CONTACT_JS = """
function handleContactSubmit(e) {
  e.preventDefault();
  const name = document.getElementById('contact-full-name').value.trim();
  alert('Thank you, ' + name + '! Your message has been received. We will contact you shortly.');
  e.target.reset();
}
"""


def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Global spacing/theme CSS
    if 'id="site-spacing-theme"' not in content:
        content = content.replace('</head>', GLOBAL_PATCH_CSS + '\n</head>', 1)

    # Make overlay more transparent in existing blocks
    content = content.replace('rgba(255, 255, 255, 0.65)', 'rgba(255, 255, 255, 0.42)')
    content = content.replace('rgba(255,255,255,0.65)', 'rgba(255,255,255,0.42)')

    basename = os.path.basename(filepath)

    # Contact section on collection pages
    if basename in COLLECTION_PAGES:
        if 'id="contact"' not in content or 'class="contact-section' not in content:
            if 'id="collection-contact-css"' not in content:
                content = content.replace('</head>', CONTACT_CSS + '\n</head>', 1)

            # Insert before footer (or bespoke-cta if no footer - insert before footer)
            footer_match = re.search(r'<footer[\s>]', content, re.I)
            if footer_match:
                pos = footer_match.start()
                content = content[:pos] + CONTACT_HTML + '\n' + content[pos:]

            if 'handleContactSubmit' not in content:
                content = content.replace('</script>', CONTACT_JS + '\n</script>', 1)

    # Reduce store.html specific large paddings
    if basename == 'store.html':
        content = re.sub(r'padding:\s*8rem\s+8%', 'padding: 4rem 6%', content)
        content = re.sub(r'padding:\s*8rem\s+5%', 'padding: 4rem 6%', content)
        content = content.replace('margin-bottom: 4.5rem', 'margin-bottom: 2rem')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Patched: {basename}')


def fix_bangles_cards():
    path = 'bangles.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove broken placeholder fragments after product-img-box closes
    content = re.sub(
        r'(</div>\s*)\s*<div class="product-img-placeholder">.*?</div>\s*<div class="gemstone-overlay-tag">.*?</div>\s*</div>\s*(<div class="product-info-box">)',
        r'\1\2',
        content,
        flags=re.DOTALL
    )
    # Card 3, 5, 6 partial broken markup
    content = re.sub(
        r'</div>\s*<div class="placeholder-label">.*?</div>\s*</div>\s*<div class="gemstone-overlay-tag">.*?</div>\s*</div>\s*(<div class="product-info-box">)',
        r'</div>\n      \1',
        content,
        flags=re.DOTALL
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Fixed bangles card HTML')


for fp in glob.glob('*.html'):
    patch_file(fp)

fix_bangles_cards()
print('Done.')
