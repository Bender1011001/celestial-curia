# The Celestial Curia - PDF Build Script
# Compiles all manuscript Markdown files into a single PDF using Pandoc

Set-Location $PSScriptRoot

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "THE CELESTIAL CURIA - PDF BUILD" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Collect all markdown files in proper order
$files = @(
    "manuscript\00_Front_Matter\00_title.md"
    "manuscript\01_Part_I_Foundations\01_Philosophical_Engine.md"
    "manuscript\01_Part_I_Foundations\02_Archetypal_Baseline.md"
    "manuscript\01_Part_I_Foundations\03_Doctrine_of_Sect.md"
    "manuscript\02_Part_II_Celestial_State\04_Essential_Dignity.md"
    "manuscript\02_Part_II_Celestial_State\05_Accidental_Dignity.md"
    "manuscript\02_Part_II_Celestial_State\06_Planetary_Delineations.md"
    "manuscript\02_Part_II_Celestial_State\07_Stars_and_Nodes.md"
    "manuscript\03_Part_III_Terrestrial_State\08_Twelve_Places.md"
    "manuscript\03_Part_III_Terrestrial_State\09_Aspects_and_Geometry.md"
    "manuscript\03_Part_III_Terrestrial_State\10_Hermetic_Lots.md"
    "manuscript\04_Part_IV_Algorithms\11_Almuten_Figuris.md"
    "manuscript\04_Part_IV_Algorithms\12_Calculus_of_Vitality.md"
    "manuscript\05_Part_V_Chronocrators\13_Hierarchy_of_Time.md"
    "manuscript\05_Part_V_Chronocrators\14_Zodiacal_Releasing.md"
    "manuscript\05_Part_V_Chronocrators\15_Firdaria.md"
    "manuscript\05_Part_V_Chronocrators\16_Annual_Profections.md"
    "manuscript\06_Part_VI_Applied_Astrology\18_Medical_Astrology.md"
    "manuscript\06_Part_VI_Applied_Astrology\19_Mundane_Astrology.md"
    "manuscript\99_Back_Matter\bibliography.md"
)

# Check which files exist
$existingFiles = @()
foreach ($file in $files) {
    if (Test-Path $file) {
        $existingFiles += $file
        Write-Host "  [OK] $file" -ForegroundColor Green
    } else {
        Write-Host "  [MISSING] $file" -ForegroundColor Yellow
    }
}

Write-Host "`nCompiling $($existingFiles.Count) files..." -ForegroundColor Cyan

# Run Pandoc
$outputFile = "The_Celestial_Curia_Draft.pdf"

try {
    $pandocArgs = @("metadata.yaml") + $existingFiles + @(
        "-o", $outputFile
        "--toc"
        "--number-sections"
        "--pdf-engine=xelatex"
        "-V", "geometry:margin=1in"
        "-V", "fontsize=11pt"
    )
    
    & pandoc @pandocArgs
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n========================================" -ForegroundColor Green
        Write-Host "BUILD SUCCESSFUL!" -ForegroundColor Green
        Write-Host "Output: $outputFile" -ForegroundColor Green
        Write-Host "========================================`n" -ForegroundColor Green
    } else {
        Write-Host "`nPandoc exited with code $LASTEXITCODE" -ForegroundColor Red
        Write-Host "Trying alternative PDF engine (pdflatex)..." -ForegroundColor Yellow
        
        $pandocArgs = @("metadata.yaml") + $existingFiles + @(
            "-o", $outputFile
            "--toc"
            "--number-sections"
            "-V", "geometry:margin=1in"
            "-V", "fontsize=11pt"
        )
        
        & pandoc @pandocArgs
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "`nBUILD SUCCESSFUL with pdflatex!" -ForegroundColor Green
            Write-Host "Output: $outputFile" -ForegroundColor Green
        }
    }
} catch {
    Write-Host "Error during compilation: $_" -ForegroundColor Red
}
