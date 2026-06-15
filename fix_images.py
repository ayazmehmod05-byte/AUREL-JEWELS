import re
import os

target_dir = r"d:\shopify store"

data = {
    "rings.html": [
        "images/model wearing rings.jpeg",
        "images/models wearing rings (2).jpeg",
        "images/models wearing rings (3).jpeg",
        "images/models wearing rings (4).jpeg",
        "images/models wearing rings (5).jpeg",
        "images/models wearing rings.jpeg"
    ],
    "earrings.html": [
        "images/model wearing earrings.jpeg",
        "images/model wearing earrings (2).jpeg",
        "images/model wearing earrings (3).jpeg",
        "images/model wearing earrings (4).jpeg",
        "images/model wearing earrings (5).jpeg",
        "images/model wearing earrings (6).jpeg"
    ],
    "necklaces.html": [
        "images/model wearing necklace.jpeg",
        "images/model wearing necklace (2).jpeg",
        "images/model wearing necklace (3).jpeg",
        "images/model wearing necklace (4).jpeg",
        "images/model wearing necklace (5).jpeg",
        "images/model wearing necklace (6).jpeg"
    ],
    "pendants.html": [
        "images/model wearing pendants.jpeg",
        "images/model wearing pendants (2).jpeg",
        "images/model wearing pendants (3).jpeg",
        "images/model wearing pendants (4).jpeg",
        "images/model wearing pendants (5).jpeg",
        "images/model wearing pendants (6).jpeg"
    ],
    "bracelets.html": [
        "images/models wearing bracelets.jpeg",
        "images/models wearing bracelets (2).jpeg",
        "images/models wearing bracelets (3).jpeg",
        "images/models wearing bracelets (4).jpeg",
        "images/models wearing bracelets (5).jpeg",
        "images/models wearing bracelets (6).jpeg"
    ],
    "bangles.html": [
        "images/models wearing bangles.jpeg",
        "images/models wearing bangles (2).jpeg",
        "images/models wearing bangles (3).jpeg",
        "images/models wearing bangles (4).jpeg",
        "images/models wearing bangles (5).jpeg",
        "images/models wearing bangles (6).jpeg"
    ]
}

for filename, images in data.items():
    filepath = os.path.join(target_dir, filename)
    if not os.path.exists(filepath):
        print(f"{filepath} not found.")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all <img src="..."> where src starts with images/
    pattern = r'(<img\s+src=")(images/[^"]+)(")'
    
    matches = list(re.finditer(pattern, content))
    
    # We expect some number of matches. If there are exactly 6 images in the cards, we replace them.
    # What if there are other images? Let's check where they are located.
    # Usually they have style="width:100%;height:300px... or alt="Product Name"
    # To be safer, let's only replace if it's within the specific card or matches "models wearing rings" etc.
    # In earrings.html we saw they were currently pointing to rings images.
    # So let's replace the first 6 matches that have src="images/model... or src="images/models..."
    
    img_index = 0
    def replacer(match):
        global img_index
        if img_index < len(images):
            # Only replace if the image is one of the target ones or looks like the placeholders we saw
            new_src = images[img_index]
            img_index += 1
            return match.group(1) + new_src + match.group(3)
        return match.group(0)

    # Let's be more specific, the cards all have alt="Product Name" or something similar.
    # Let's replace only images that are inside the <div class="product-card"> or simply the first 6 images that match `images/model.*`
    
    pattern_specific = r'(<img\s+src=")(images/models? wearing[^"]+)(")'
    
    img_index = 0
    new_content = re.sub(pattern_specific, replacer, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {filename}: replaced {img_index} images.")
