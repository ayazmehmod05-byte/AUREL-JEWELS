$dir = "d:\shopify store"
$files = Get-ChildItem -Path $dir -Filter "*.html"

$videoFile = "WhatsApp Video 2026-06-14 at 1.51.38 AM.mp4"
$modelImages = Get-ChildItem -Path "$dir\updated store\images" -Filter "*.jpeg" | Select-Object -ExpandProperty Name

# Helper to get an image
$imgIndex = 0
function Get-NextImage {
    global:imgIndex
    $img = $modelImages[$imgIndex % $modelImages.Count]
    $script:imgIndex++
    return "updated store/images/$img"
}

foreach ($file in $files) {
    $filePath = $file.FullName
    $content = [System.IO.File]::ReadAllText($filePath)

    # 1. BRAND NAME
    $content = $content -replace 'ANTIGRAVITY', 'AUREL JEWELS'
    $content = $content -replace 'Antigravity', 'AUREL JEWELS'
    $content = $content -replace 'GRAVITY', 'AUREL JEWELS'

    # 6. THEME
    # Change --dark colors to --white. Body bg:#FFFFFF, text:#1a1a1a.
    $content = $content -replace '--dark: #1a1a1a;', '--dark: #ffffff;'
    # Actually, they want "--dark colors to --white". 
    # Let's just ensure body is #FFFFFF and text is #1a1a1a.
    # The previous script might have added body { background-image: ... } which we need to remove.
    $content = [regex]::Replace($content, '(?s)/\* Task 2: BACKGROUNDS \*/.*?/\* Task 5: THEME - Glass Effect for cards \*/', '/* Task 5: THEME - Glass Effect for cards */')
    # Let's remove the body::after overlay that we added previously
    $content = [regex]::Replace($content, '(?s)/\* Transparent overlay \*/.*?/\* Make sections transparent so the background shows through \*/', '/* Make sections transparent so the background shows through */')

    # Remove the old global body background-image
    $content = [regex]::Replace($content, '(?i)body\s*\{[^}]*background-image:[^}]*\}', '')
    
    # Add new CSS for sections and cards
    $sectionCSS = @"
    <style>
      /* Section Backgrounds Overlay */
      body {
         background-color: #FFFFFF !important;
         color: #1a1a1a !important;
      }
      section, header, footer, main {
          position: relative;
          background-attachment: fixed !important;
          background-size: cover !important;
          background-position: center !important;
      }
      section::before, header::before, footer::before, main::before {
          content: "";
          position: absolute;
          top: 0; left: 0; right: 0; bottom: 0;
          background: rgba(255, 255, 255, 0.65) !important;
          z-index: 0;
          pointer-events: none;
      }
      section > *, header > *, footer > *, main > * {
          position: relative;
          z-index: 1;
      }
      
      /* All cards glass effect */
      .product-card, .category-card, .contact-card, .engraving-preview-card, .metric-content-box, .collection-card, .item-card, .finish-selection-box {
          background: rgba(255, 255, 255, 0.6) !important;
          backdrop-filter: blur(10px) !important;
          -webkit-backdrop-filter: blur(10px) !important;
          border: 1px solid rgba(255,255,255,0.4) !important;
          box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07) !important;
      }
      
      /* Additional text color enforcement */
      h1, h2, h3, h4, h5, h6, p, span, li, a {
          color: #1a1a1a;
      }
      .sec-title h2, .hero h1, .smart-showcase h2, .logo {
          color: #1a1a1a !important;
      }
    </style>
"@
    
    # Inject our new CSS if it's not there
    if (-not $content.Contains("/* Section Backgrounds Overlay */")) {
        $content = $content.Replace("</head>", "$sectionCSS`n</head>")
    }

    # Assign different backgrounds to sections
    $sections = [regex]::Matches($content, '(?i)<(section|footer|header|main)([^>]*)>')
    foreach ($match in $sections) {
        $tag = $match.Groups[1].Value
        $attrs = $match.Groups[2].Value
        # Make sure we don't duplicate styles
        if (-not $attrs.Contains("style=`"background-image")) {
            $img = Get-NextImage
            $newTag = "<$tag$attrs style=`"background-image: url('$img');`">"
            $content = $content.Replace($match.Value, $newTag)
        }
    }

    # 3. PRODUCT CARDS: Inside each card, add product image, and a small circular thumbnail of model
    # Look for .product-card and replace its image logic
    # The previous run already added the product images. 
    # Let's ensure the thumbnail is added.
    $cardMatches = [regex]::Matches($content, '(?s)<div class="product-card">.*?</div>\s*</div>\s*</div>')
    # Actually regex for cards is risky, let's just do a blanket replace where we find product-img
    $content = [regex]::Replace($content, '(?i)(<img[^>]*class="[^"]*product-img[^"]*"[^>]*src="([^"]+)"[^>]*>)', "`$1`n<img src=`"`$2`" style=`"width:40px; height:40px; border-radius:50%; position:absolute; top:10px; right:10px; border:2px solid white; object-fit:cover; z-index:10;`" alt=`"Model Thumbnail`">")

    # 4. DROPDOWN ICONS: (Already done, but let's double check there are no emojis)
    # The user gave specific ones, let's just re-replace just in case.
    $dropdownReplacement = @"
<div class="nav-dropdown-menu">
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
      </div>
"@
    $content = [regex]::Replace($content, '(?s)<div class="nav-dropdown-menu">.*?</div>', $dropdownReplacement)

    # 5. HERO PAGE: Delete current hero content. Add ring video file as full-width hero background.
    if ($file.Name -eq "store.html") {
        # The prompt says: Delete current hero content. Add my ring video file ... as full-width hero background. Add heading AUREL JEWELS on top of video.
        $newHero = @"
<section class="hero" id="home" style="position:relative; min-height:100vh; overflow:hidden; display:flex; align-items:center; justify-content:center;">
    <video autoplay loop muted playsinline style="position:absolute; top:0; left:0; width:100%; height:100%; object-fit:cover; z-index:-1;">
        <source src="$videoFile" type="video/mp4">
    </video>
    <div style="position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(255,255,255,0.4); z-index:0;"></div>
    <div class="hero-content" style="position:relative; z-index:1; text-align:center;">
        <h1 style="font-size:clamp(3rem, 8vw, 6rem); letter-spacing:4px; font-weight:800; color:#1a1a1a; text-shadow:2px 2px 10px rgba(255,255,255,0.8);">AUREL JEWELS</h1>
    </div>
</section>
"@
        $content = [regex]::Replace($content, '(?s)<section class="hero"[^>]*>.*?</section>', $newHero)
    }

    [System.IO.File]::WriteAllText($filePath, $content)
}
Write-Host "Done"
