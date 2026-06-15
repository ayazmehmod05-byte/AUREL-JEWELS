"""Fix contact JS and aureljewels local images."""
import re
import glob

CONTACT_JS = """
function handleContactSubmit(e) {
  e.preventDefault();
  const name = document.getElementById('contact-full-name').value.trim();
  alert('Thank you, ' + name + '! Your message has been received. We will contact you shortly.');
  e.target.reset();
}
"""

SEC_TITLE_CSS = """
      .sec-title {
        text-align: center;
        margin-bottom: 2rem;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
      }
      .sec-title span {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        color: #D4AF37;
        font-weight: 600;
        display: block;
        margin-bottom: 0.6rem;
      }
      .sec-title h2 {
        font-family: 'Playfair Display', serif;
        font-size: clamp(1.8rem, 4vw, 2.8rem);
        font-weight: 600;
        line-height: 1.25;
      }
      .sec-title p {
        color: #7a7a85;
        margin-top: 0.75rem;
        font-size: 0.95rem;
      }
"""

for page in ['earrings.html', 'necklaces.html', 'pendants.html', 'bracelets.html', 'bangles.html']:
    with open(page, 'r', encoding='utf-8') as f:
        c = f.read()
    if 'function handleContactSubmit' not in c:
        c = c.replace('</body>', '<script>' + CONTACT_JS + '</script>\n</body>')
    if SEC_TITLE_CSS.strip() not in c and 'collection-contact-css' in c:
        c = c.replace('<style id="collection-contact-css">', '<style id="collection-contact-css">' + SEC_TITLE_CSS)
    with open(page, 'w', encoding='utf-8') as f:
        f.write(c)
    print('Fixed', page)

# Aurel jewels: local backgrounds + model card images
AUREL_BG = {
    'earrings': 'updated store/images/WhatsApp Image 2026-06-14 at 1.10.29 AM (1).jpeg',
    'necklaces': 'updated store/images/WhatsApp Image 2026-06-14 at 1.10.30 AM.jpeg',
    'pendants': 'updated store/images/WhatsApp Image 2026-06-14 at 1.10.27 AM (1).jpeg',
    'bracelets': 'updated store/images/WhatsApp Image 2026-06-14 at 1.10.28 AM (2).jpeg',
    'bangles': 'updated store/images/WhatsApp Image 2026-06-14 at 1.10.31 AM (1).jpeg',
}
AUREL_IMGS = {
    'rings': [
        'images/model wearing rings.jpeg', 'images/models wearing rings (2).jpeg',
        'images/models wearing rings (3).jpeg', 'images/models wearing rings (4).jpeg',
        'images/models wearing rings (5).jpeg', 'images/model wearing rings.jpeg',
    ],
    'earrings': [
        'images/models wearing earrings.jpeg', 'images/models wearing earrings (2).jpeg',
        'images/models wearing earrings (3).jpeg', 'images/models wearing earrings (4).jpeg',
        'images/models wearing earrings (5).jpeg', 'images/models wearing earrings (6).jpeg',
    ],
    'necklaces': [
        'images/models wearing necklaces.jpeg', 'images/models wearing necklaces (2).jpeg',
        'images/models wearing necklaces (3).jpeg', 'images/models wearing necklaces (4).jpeg',
        'images/models wearing necklaces (5).jpeg', 'images/models wearing necklaces (6).jpeg',
    ],
    'pendants': [
        'images/models wearing pendant.jpeg', 'images/models wearing pendant (2).jpeg',
        'images/models wearing pendant (3).jpeg', 'images/models wearing pendant (4).jpeg',
        'images/models wearing pendant (5).jpeg', 'images/models wearing pendant (6).jpeg',
    ],
    'bracelets': [
        'images/models wearing bracelets.jpeg', 'images/models wearing bracelets (2).jpeg',
        'images/models wearing bracelets (3).jpeg', 'images/models wearing bracelets (4).jpeg',
        'images/models wearing bracelets (5).jpeg', 'images/models wearing bracelets (6).jpeg',
    ],
    'bangles': [
        'images/models wearing bangles.jpeg', 'images/models wearing bangles (2).jpeg',
        'images/models wearing bangles (3).jpeg', 'images/models wearing bangles (4).jpeg',
        'images/models wearing bangles (5).jpeg', 'images/models wearing bangles (6).jpeg',
    ],
}

with open('aureljewels.html', 'r', encoding='utf-8') as f:
    aurel = f.read()

for sec_id, bg in AUREL_BG.items():
    aurel = re.sub(
        rf'(<section id="{sec_id}"[^>]*style=")background-image:url\([^)]+\)',
        rf'\1background-image:url(\'{bg}\')',
        aurel,
        count=1
    )
    aurel = re.sub(
        rf'(<section id="{sec_id}"[^>]*)py-16 sm:py-20',
        r'\1py-12 sm:py-16',
        aurel,
        count=1
    )

for cat, imgs in AUREL_IMGS.items():
    section_match = re.search(rf'<section id="{cat}"[\s\S]*?</section>', aurel)
    if not section_match:
        continue
    section = section_match.group(0)
    idx = 0
    def repl_img(m):
        global_idx = idx
        # use local counter inside closure
        return m.group(0)
    new_section = section
    for i, img in enumerate(imgs):
        new_section = re.sub(
            r'src="https://images\.unsplash\.com/[^"]*"',
            f'src="{img}"',
            new_section,
            count=1
        )
    aurel = aurel[:section_match.start()] + new_section + aurel[section_match.end():]

aurel = re.sub(r'py-16 sm:py-20', 'py-12 sm:py-16', aurel)
aurel = aurel.replace("style=\"background:#fff;\" style=", "style=")

with open('aureljewels.html', 'w', encoding='utf-8') as f:
    f.write(aurel)
print('Updated aureljewels.html')

# Add sec-title to rings contact css
with open('rings.html', 'r', encoding='utf-8') as f:
    r = f.read()
if SEC_TITLE_CSS.strip() not in r:
    r = r.replace('<style id="collection-contact-css">', '<style id="collection-contact-css">' + SEC_TITLE_CSS)
    with open('rings.html', 'w', encoding='utf-8') as f:
        f.write(r)
print('Done')
