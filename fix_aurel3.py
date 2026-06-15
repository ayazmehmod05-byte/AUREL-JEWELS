import glob
import re
import random

files = glob.glob('*.html')

# Model images
images = glob.glob('updated store/images/*.jpeg')
def get_image():
    global img_idx
    if len(images) == 0: return ""
    img = images[img_idx % len(images)]
    img_idx += 1
    return img.replace('\\', '/')

img_idx = 0

dropdown_replacement = """      <div class="nav-dropdown-menu" id="collections-menu">
        <a href="rings.html" class="dropdown-item">
          <i class="fa-solid fa-ring"></i> Rings
        </a>
        <a href="earrings.html" class="dropdown-item">
          <i class="fa-solid fa-ear-listen"></i> Earrings
        </a>
        <a href="necklaces.html" class="dropdown-item">
          <i class="fa-solid fa-link"></i> Necklaces
        </a>
        <a href="pendants.html" class="dropdown-item">
          <i class="fa-solid fa-gem"></i> Pendants
        </a>
        <div class="dropdown-divider"></div>
        <a href="bracelets.html" class="dropdown-item">
          <i class="fa-solid fa-circle-notch"></i> Bracelets
        </a>
        <a href="bangles.html" class="dropdown-item">
          <i class="fa-solid fa-circle"></i> Bangles
        </a>
      </div>"""

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. FIX BRAND NAME
    content = content.replace('ANTI<span>AUREL JEWELS</span>', 'AUREL <span>JEWELS</span>')
    content = content.replace('ANTI<span>GRAVITY</span>', 'AUREL <span>JEWELS</span>')
    content = content.replace('ANTIGRAVITY', 'AUREL JEWELS')
    content = content.replace('GRAVITY', 'AUREL JEWELS')
    content = content.replace('Antigravity', 'AUREL JEWELS')

    # 2. FIX DROPDOWN
    # We replace from <div class="nav-dropdown-menu" up to the </div> that closes Bangles </a>
    # A safe way is to replace the whole block by finding the opening and an anchor to Bangles
    dropdown_match = re.search(r'<div class="nav-dropdown-menu"[^>]*>.*?Bangles\s*</a>\s*</div>', content, re.DOTALL)
    if dropdown_match:
        content = content.replace(dropdown_match.group(0), dropdown_replacement)

    # 3. FIX PRODUCT CARDS
    # We have two types of cards:
    # A) "Add Product Image" boxes:
    # <div class="card-image"> ... <span class="card-image-label">Add Product Image</span> ... </div>
    # or <p class="card-image-text">Add Product Image</p>
    
    def replace_add_product_box(match):
        img = get_image()
        thumb = get_image()
        inner_content = match.group(0)
        # We replace the text with an image, and add thumbnail
        # Let's just wipe out the label/text and insert images
        new_content = re.sub(r'<span class="card-image-label">Add Product Image</span>', '', inner_content)
        new_content = re.sub(r'<p class="card-image-text">Add Product Image</p>', '', new_content)
        new_content = re.sub(r'<div class="card-image-icon">\+</div>', '', new_content)
        
        # Insert image tags right inside <div class="card-image">
        # To do this safely, we add them at the end before </div>
        images_html = f'\n          <img src="{img}" class="product-img" style="width:100%; height:100%; object-fit:cover;">\n'
        images_html += f'          <img src="{thumb}" style="width:40px; height:40px; border-radius:50%; position:absolute; top:15px; right:15px; border:2px solid #fff; object-fit:cover; z-index:10; box-shadow:0 4px 10px rgba(0,0,0,0.1);" alt="Model thumbnail">\n'
        
        return new_content.replace('</div>', images_html + '        </div>', 1)

    content = re.sub(r'<div class="card-image">.*?Add Product Image.*?</div>', replace_add_product_box, content, flags=re.DOTALL)

    # B) Existing images without thumbnails (like in store.html)
    # <div class="product-img-box"> ... <img src="..."> ... </div>
    # We'll just find <img src="..."> inside product-img-box or card-image that doesn't have the thumbnail yet.
    # To be safe and simple: find <img src="..." alt="..."> inside product-img-box
    
    def add_thumbnail_to_existing(match):
        inner = match.group(0)
        if 'Model thumbnail' in inner: return inner
        thumb = get_image()
        # Find the main img and append thumbnail
        main_img_match = re.search(r'<img[^>]+>', inner)
        if main_img_match:
            main_img = main_img_match.group(0)
            if 'Model thumbnail' not in main_img:
                thumb_html = f'\n<img src="{thumb}" style="width:40px; height:40px; border-radius:50%; position:absolute; top:15px; right:15px; border:2px solid #fff; object-fit:cover; z-index:10; box-shadow:0 4px 10px rgba(0,0,0,0.1);" alt="Model thumbnail">\n'
                return inner.replace(main_img, main_img + thumb_html)
        return inner

    content = re.sub(r'<div class="product-img-box">.*?</div>', add_thumbnail_to_existing, content, flags=re.DOTALL)

    # 4. CARD GLASS EFFECT CSS & TEXT COLORS
    css_to_add = """
    <style>
      .card, .product-card, .category-card {
         background: rgba(255,255,255,0.6) !important;
         backdrop-filter: blur(10px) !important;
         -webkit-backdrop-filter: blur(10px) !important;
         border: 1px solid rgba(255,255,255,0.4) !important;
      }
      body { background-color: #FFFFFF !important; color: #1a1a1a !important; }
      h1, h2, h3, h4, h5, h6, p, span, div, a, li { color: #1a1a1a; }
      .logo { color: #1a1a1a !important; }
      .logo span { color: #1a1a1a !important; } /* If they want it all black, or we can leave span gold */
    </style>
    """
    if "backdrop-filter: blur(10px)" not in content:
        content = content.replace("</head>", css_to_add + "</head>")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("HTML processing complete.")
