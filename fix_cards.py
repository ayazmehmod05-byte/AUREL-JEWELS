import glob
import re
import os

files = glob.glob('*.html')

def get_images(category):
    all_imgs = [f.replace('\\', '/') for f in glob.glob('images/*.jpeg')]
    res = []
    for f in all_imgs:
        f_lower = f.lower()
        if category == 'rings':
            # "wearing" has "ring" in it, so we must be careful.
            # Look for " rings" or " ring" but not "earring"
            if (' rings' in f_lower or ' ring' in f_lower) and 'earring' not in f_lower:
                res.append(f)
        elif category == 'earrings':
            if 'earring' in f_lower: res.append(f)
        elif category == 'necklaces':
            if 'necklace' in f_lower: res.append(f)
        elif category == 'pendants':
            if 'pendant' in f_lower: res.append(f)
        elif category == 'bracelets':
            if 'bracelet' in f_lower: res.append(f)
        elif category == 'bangles':
            if 'bangle' in f_lower: res.append(f)
    return res

categories = {
    'rings': get_images('rings'),
    'earrings': get_images('earrings'),
    'necklaces': get_images('necklaces'),
    'pendants': get_images('pendants'),
    'bracelets': get_images('bracelets'),
    'bangles': get_images('bangles')
}

counters = {k: 0 for k in categories.keys()}

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine which category this file belongs to
    page_cat = None
    for cat in categories.keys():
        if cat in filepath.lower():
            page_cat = cat
            break
            
    if not page_cat: page_cat = 'rings'

    def replace_card_image(match):
        imgs = categories[page_cat]
        if not imgs:
            img_src = "images/placeholder.jpg"
        else:
            img_src = imgs[counters[page_cat] % len(imgs)]
            counters[page_cat] += 1
            
        return f'<div class="card-image">\n          <img src="{img_src}" alt="Product Name" style="width:100%;height:300px;object-fit:cover;border-radius:12px;">\n        </div>'

    content = re.sub(r'<div class="card-image">\n          <img src="[^"]*" alt="Product Name" style="width:100%;height:300px;object-fit:cover;border-radius:12px;">\n        </div>', replace_card_image, content, flags=re.DOTALL)
    
    def replace_product_img_box(match):
        imgs = categories[page_cat]
        if not imgs:
            img_src = "images/placeholder.jpg"
        else:
            img_src = imgs[counters[page_cat] % len(imgs)]
            counters[page_cat] += 1
            
        return f'<div class="product-img-box">\n        <img src="{img_src}" alt="Product Name" style="width:100%;height:300px;object-fit:cover;border-radius:12px;">\n      </div>'

    content = re.sub(r'<div class="product-img-box">\n        <img src="[^"]*" alt="Product Name" style="width:100%;height:300px;object-fit:cover;border-radius:12px;">\n      </div>', replace_product_img_box, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Images replaced precisely.")
