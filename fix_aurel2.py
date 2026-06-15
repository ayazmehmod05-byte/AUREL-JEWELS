import glob
import re

files = glob.glob('*.html')

dropdown_replacement = """      <div class="nav-dropdown-menu">
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
        lines = f.readlines()
    
    new_lines = []
    in_dropdown = False
    dropdown_divs_count = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # DROPDOWN REPLACEMENT
        if '<div class="nav-dropdown-menu">' in line:
            in_dropdown = True
            new_lines.append(dropdown_replacement + '\n')
            
            # Now we must skip lines until this dropdown is closed
            # Count the opening div we just hit
            dropdown_divs_count = 1
            i += 1
            while i < len(lines) and dropdown_divs_count > 0:
                if '<div' in lines[i]:
                    dropdown_divs_count += lines[i].count('<div')
                if '</div' in lines[i]:
                    dropdown_divs_count -= lines[i].count('</div')
                i += 1
            # After this loop, we have skipped the whole nav-dropdown-menu
            in_dropdown = False
            continue
        
        # PRODUCT THUMBNAIL
        # Look for the product image, e.g., <img class="product-img" src="..." or <img src="..." class="product-img"
        new_lines.append(line)
        if 'class="product-img"' in line or 'class="product-img"' in lines[i-1] if i>0 else False:
            # wait, let's just check the current line for product-img
            # Actually, to be safe, find any img tag that has product-img in it
            if '<img' in line and 'product-img' in line and 'alt="Model thumbnail"' not in line:
                # extract src using regex
                src_match = re.search(r'src="([^"]+)"', line)
                if src_match:
                    src = src_match.group(1)
                    thumb_html = f'          <img src="{src}" style="width:40px; height:40px; border-radius:50%; position:absolute; top:15px; right:15px; border:2px solid #fff; object-fit:cover; z-index:10; box-shadow:0 4px 10px rgba(0,0,0,0.1);" alt="Model thumbnail">\n'
                    new_lines.append(thumb_html)
                    
        i += 1

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

print("HTML processing complete.")
