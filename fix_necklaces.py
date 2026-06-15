import re
import os

target_file = r"d:\shopify store\necklaces.html"

images = [
    "images/model wearing necklace.jpeg",
    "images/model wearing necklace (2).jpeg",
    "images/model wearing necklace (3).jpeg",
    "images/model wearing necklace (4).jpeg",
    "images/model wearing necklace (5).jpeg",
    "images/model wearing necklace (6).jpeg"
]

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find <div class="card-placeholder">...</div>
# We can use a regex that matches from <div class="card-placeholder"> up to the next </div></div> (since it has nested divs)
# But it's easier to just write a simple regex or use a string replacement loop
# The placeholder is exactly:
'''
          <div class="card-placeholder">
            <span class="placeholder-icon">...</span>
            <div class="placeholder-lines">
              <div class="placeholder-line"></div>
              <div class="placeholder-line"></div>
            </div>
          </div>
'''
pattern = r'<div class="card-placeholder">.*?</div>\s*</div>\s*</div>'
# wait, <div class="card-placeholder">...</div> has a span, and a div with 2 divs. That's 4 closing divs.
# Let's use re.DOTALL to replace from <div class="card-placeholder"> up to the correct </div>
pattern = r'<div class="card-placeholder">.*?</div>\s*</div>\s*</div>'

# Actually, an easier way is to find <div class="card-placeholder"> and replace the whole block.
# Let's write a python script that replaces the n-th card-placeholder.

import re
pattern = re.compile(r'<div class="card-placeholder">.*?</div>\s*</div>\s*</div>', re.DOTALL)

img_index = 0
def replacer(match):
    global img_index
    if img_index < len(images):
        new_src = images[img_index]
        img_index += 1
        return f'<img src="{new_src}" alt="Product Name" style="width:100%;height:300px;object-fit:cover;border-radius:12px;">'
    return match.group(0)

new_content = pattern.sub(replacer, content)

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Updated necklaces.html: replaced {img_index} placeholders.")
