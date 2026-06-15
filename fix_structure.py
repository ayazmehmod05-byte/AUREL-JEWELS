import re

# Fix pendants.html
with open('pendants.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern for pendants.html
# We want to remove the extra </div> between </button> (from wishlist-btn) and <div class="product-info-box">
pattern_pendants = r'(<button class="wishlist-btn" aria-label="Add to wishlist">♡</button>\s*)</div>(\s*<div class="product-info-box">)'
content, count = re.subn(pattern_pendants, r'\1\2', content)
print(f"Fixed {count} mismatched divs in pendants.html")

with open('pendants.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Fix bracelets.html
with open('bracelets.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern for bracelets.html
# We want to remove the extra </div> between the quick-add-overlay </div> and <div class="product-info-box">
# Look for:
#           </div>
#         </div>
#         <div class="product-info-box">
# We want to keep only one </div> before <div class="product-info-box">
# Let's use a very specific pattern:
pattern_bracelets = r'(<div class="quick-add-overlay">.*?</div>\s*)</div>(\s*<div class="product-info-box">)'
content, count = re.subn(pattern_bracelets, r'\1\2', content, flags=re.DOTALL)
print(f"Fixed {count} mismatched divs in bracelets.html")

with open('bracelets.html', 'w', encoding='utf-8') as f:
    f.write(content)
