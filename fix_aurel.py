import os
import re
import glob

# Get all html files
files = glob.glob('*.html')

dropdown_content = """<div class="nav-dropdown-menu">
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

    # 1. Fix the dropdown menu. We need to match from <div class="nav-dropdown-menu"> up to the </div> that closes it.
    # The block ends right before <div class="nav-actions"> or similar.
    # Let's match from <div class="nav-dropdown-menu"> up to the </div>\s*</div>
    # Actually, a better way is to find the exact old block we know is there:
    old_dropdown_pattern = re.compile(r'<div class="nav-dropdown-menu">.*?Bangles\s*</a>\s*</div>', re.DOTALL)
    content = old_dropdown_pattern.sub(dropdown_content, content)
    
    # 2. Add product thumbnails.
    # The requirement: Inside each card, add product image from images/ folder. Also add small circular thumbnail of model wearing that same product.
    # The cards are typically <div class="product-card"> or something similar.
    # Let's find <img src="updated store/images/..." class="product-img" ...> 
    # Or just find the product-img tag and inject a thumbnail right after it.
    
    def replace_img(match):
        img_tag = match.group(0)
        src_match = re.search(r'src="([^"]+)"', img_tag)
        if src_match:
            src = src_match.group(1)
            # Add thumbnail right after the main image
            thumb = f'\n<img src="{src}" style="width:40px; height:40px; border-radius:50%; position:absolute; top:15px; right:15px; border:2px solid #fff; object-fit:cover; z-index:10; box-shadow:0 4px 10px rgba(0,0,0,0.1);" alt="Model thumbnail">'
            return img_tag + thumb
        return img_tag

    # Find all images with class product-img, but don't add thumbnail if it's already there
    if 'alt="Model thumbnail"' not in content:
        content = re.sub(r'<img[^>]*class="[^"]*product-img[^"]*"[^>]*>', replace_img, content)

    # Make sure text colors are dark globally in the CSS since body is white
    # The previous PS script added h1, h2, etc. Let's make sure it covers more and is specific
    color_css = """
      /* Text Colors override for white theme */
      body, p, span, div, a, li { color: #1a1a1a; }
      h1, h2, h3, h4, h5, h6, .sec-title h2, .hero h1, .smart-showcase h2, .logo { color: #1a1a1a !important; }
      .category-overlay h3, .product-info-box h3 { color: #1a1a1a !important; }
      .dropdown-item { color: #1a1a1a !important; }
      .nav-links a { color: #1a1a1a !important; }
"""
    if '/* Text Colors override for white theme */' not in content:
        content = content.replace('/* Additional text color enforcement */', color_css)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done with Python script")
