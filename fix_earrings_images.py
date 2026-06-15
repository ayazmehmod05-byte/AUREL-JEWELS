import re

earrings_images = [
    "images/models wearing earrings.jpeg",
    "images/models wearing earings.jpeg",
    "images/model wearing earrings.jpeg",
    "images/model wearing earrings (2).jpeg",
    "images/model wearing earrings (3).jpeg",
    "images/model wearing earrings (4).jpeg"
]

# 1. Update earrings.html
with open('earrings.html', 'r', encoding='utf-8') as f:
    content = f.read()

# We want to replace the first 6 image tags inside the product cards
# Let's find all occurrences of:
# <div class="card-image">
#           <img src="images/[^"]*"
# or simply replace the image source within the product-grid.
# We can search for the product-grid block and substitute card-by-card.
# To be robust, let's match the exact src attributes inside <div class="card-image">

grid_match = re.search(r'<div class="product-grid" id="productGrid">.*?</div>\s*</section>', content, re.DOTALL)
if grid_match:
    grid_html = grid_match.group(0)
    
    # We will find all <img src="images/[^"]*" inside grid_html and replace them sequentially
    img_pattern = r'(<div class="card-image">\s*<img src=")(images/[^"]*)(")'
    matches = list(re.finditer(img_pattern, grid_html))
    print(f"Found {len(matches)} image matches in earrings.html grid")
    
    new_grid_html = grid_html
    offset = 0
    for i, m in enumerate(matches[:6]):
        new_src = earrings_images[i]
        start = m.start(2) + offset
        end = m.end(2) + offset
        new_grid_html = new_grid_html[:start] + new_src + new_grid_html[end:]
        offset += len(new_src) - (m.end(2) - m.start(2))
        
    content = content.replace(grid_html, new_grid_html)
    with open('earrings.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated earrings.html with correct earrings images.")
else:
    print("Could not find product-grid in earrings.html")


# 2. Update aureljewels.html (earrings section)
with open('aureljewels.html', 'r', encoding='utf-8') as f:
    content = f.read()

section_match = re.search(r'<section id="earrings".*?</section>', content, re.DOTALL)
if section_match:
    section_html = section_match.group(0)
    
    # Find all <img src="images/[^"]*" inside section_html
    img_pattern = r'(<img\s+src=")(images/[^"]+)(")'
    matches = list(re.finditer(img_pattern, section_html))
    print(f"Found {len(matches)} image matches in aureljewels.html earrings section")
    
    new_section_html = section_html
    offset = 0
    for i, m in enumerate(matches[:6]):
        new_src = earrings_images[i]
        start = m.start(2) + offset
        end = m.end(2) + offset
        new_section_html = new_section_html[:start] + new_src + new_section_html[end:]
        offset += len(new_src) - (m.end(2) - m.start(2))
        
    content = content.replace(section_html, new_section_html)
    with open('aureljewels.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated aureljewels.html with correct earrings images.")
else:
    print("Could not find earrings section in aureljewels.html")
