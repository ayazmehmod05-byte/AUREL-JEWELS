$dir = "d:\shopify store"
$files = Get-ChildItem -Path $dir -Filter "*.html"

$ringVideo = "WhatsApp Video 2026-06-14 at 1.51.38 AM.mp4"
$modelImages = Get-ChildItem -Path "$dir\updated store\images" -Filter "*.jpeg" | Select-Object -ExpandProperty Name
$bgImage = "updated store/images/" + $modelImages[0]

$dropdownReplacement = @"
<div class="nav-dropdown-menu">
        <a href="rings.html" class="dropdown-item">
          <span class="dropdown-item-icon fa-solid fa-ring"></span> Rings
        </a>
        <a href="earrings.html" class="dropdown-item">
          <span class="dropdown-item-icon fa-solid fa-ear-listen"></span> Earrings
        </a>
        <a href="necklaces.html" class="dropdown-item">
          <span class="dropdown-item-icon fa-solid fa-link"></span> Necklaces
        </a>
        <a href="pendants.html" class="dropdown-item">
          <span class="dropdown-item-icon fa-solid fa-gem"></span> Pendants
        </a>
        <div class="dropdown-divider"></div>
        <a href="bracelets.html" class="dropdown-item">
          <span class="dropdown-item-icon fa-solid fa-circle-notch"></span> Bracelets
        </a>
        <a href="bangles.html" class="dropdown-item">
          <span class="dropdown-item-icon fa-solid fa-circle"></span> Bangles
        </a>
      </div>
"@

$globalCSS = @"
  <style>
    /* Task 2: BACKGROUNDS */
    body {
      background-image: url('$bgImage') !important;
      background-attachment: fixed !important;
      background-size: cover !important;
      background-position: center !important;
      position: relative;
    }
    
    /* Transparent overlay */
    body::after {
      content: "";
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(255, 255, 255, 0.65) !important;
      z-index: -999;
      pointer-events: none;
    }

    /* Make sections transparent so the background shows through */
    section, header, footer, main, .hero, .smart-showcase, .engraving-section, .collections-grid, .bg-light, .bg-dark {
      background: transparent !important;
      background-color: transparent !important;
    }

    /* Task 5: THEME - Glass Effect for cards */
    .product-card, .category-card, .contact-card, .engraving-preview-card, .metric-content-box, .collection-card, .item-card, .finish-selection-box {
      background: rgba(255, 255, 255, 0.6) !important;
      backdrop-filter: blur(10px) !important;
      -webkit-backdrop-filter: blur(10px) !important;
      border: 1px solid rgba(255,255,255,0.4) !important;
      box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07) !important;
    }
    
    /* Ensure text is visible and layout correct */
    .smart-showcase h2, .smart-showcase p, .smart-showcase h3, .smart-showcase li, .smart-showcase span {
      color: #1a1a1a !important;
    }
  </style>
</head>
"@

$imgMap = @{
    'rings' = $modelImages[1]
    'earrings' = $modelImages[2]
    'necklaces' = $modelImages[3]
    'pendants' = $modelImages[4]
    'bracelets' = $modelImages[5]
    'bangles' = $modelImages[6]
    'store' = $modelImages[7]
}

foreach ($file in $files) {
    $filePath = $file.FullName
    $content = [System.IO.File]::ReadAllText($filePath)
    
    # Task 1: Dropdown
    $content = [regex]::Replace($content, '(?s)<div class="nav-dropdown-menu">.*?</div>', $dropdownReplacement)
    $content = [regex]::Replace($content, '(?s)\.dropdown-item-icon:not\(\.fa-solid\)\s*\{\s*display:\s*none;\s*\}', '')
    
    # Task 4: HERO in store.html
    if ($file.Name -eq "store.html") {
        $heroReplacement = '<div class="hero-image-wrapper"><video autoplay loop muted playsinline style="width:100%; max-width:480px; height:500px; object-fit:cover; border-radius:24px; border:1px solid rgba(201,169,97,0.4); box-shadow:0 25px 60px rgba(0,0,0,0.12); z-index:2;"><source src="' + $ringVideo + '" type="video/mp4"></video></div>'
        $content = [regex]::Replace($content, '(?s)<div class="hero-image-wrapper">.*?</div>\s*</div>', "$heroReplacement</div>")
    }

    # Task 2 & 5: CSS
    if (-not $content.Contains("/* Task 2: BACKGROUNDS */")) {
        $content = $content.Replace("</head>", $globalCSS)
    }

    # Task 3: Product Cards images
    $pageType = $file.Name.Replace('.html', '')
    if ($imgMap.ContainsKey($pageType)) {
        $imgName = $imgMap[$pageType]
        # Replace product image src
        $content = [regex]::Replace($content, '(?i)<img([^>]*)class="([^"]*)product-img([^"]*)"([^>]*)src="[^"]*"([^>]*)>', "<img`$1class=`"`$2product-img`$3`"`$4src=`"updated store/images/$imgName`"`$5>")
        # fallback if src is before class
        $content = [regex]::Replace($content, '(?i)<img([^>]*)src="[^"]*"([^>]*)class="([^"]*)product([^"]*)"([^>]*)>', "<img`$1src=`"updated store/images/$imgName`"`$2class=`"`$3product`$4`"`$5>")
    }

    [System.IO.File]::WriteAllText($filePath, $content)
}

Write-Host "Done"
