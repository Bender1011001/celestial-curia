$files = @(
    "Astrology Codex_ Pre-1700 Interpretations.txt",
    "Researching Ancient Astrological Datasets.txt",
    "Traditional Astrology's Core Mechanics.txt",
    "The Archetypal Baseline_ Thema Mundi, Aspect Natures, and the Philosophical Divide Between Egyptian and Ptolemaic Terms.txt",
    "_The Hierarchy of Celestial Causation_ Universal and Particular Causes in Classical Astrology.txt",
    "Technical Analysis_ Ptolemaic Eclipse Mechanics and the Substitute King Protocol as Evidence of Conditional Fate.txt",
    "_The Binary Competency Framework of Classical Astrology_ Sect, Solar Proximity, and Bonatti's Considerations as Deterministic Rules of Planetary Engagement.txt",
    "_The Jurisprudential Audit Framework.txt",
    "_The Ministerial Order of Celestial Authority_ Ibn Ezra's Algorithm and the Calculus of Vitality.txt",
    "Comprehensive Treatment of Houses, Planetary Delineations, Dignities, and Aspects in Traditional Astrology.txt",
    "Planetary Delineations From Ancient Sources.txt",
    "# Section Five Monomoiria—The Micro.txt",
    "Section_2_Lunar_Nodes.txt",
    "Section_3_Fixed_Stars.txt",
    "Section_1_Arabic_Parts.txt",
    "Traditional Time-Lord Systems Research.txt",
    "The Nested Hierarchy of Chronocrators_ Dormancy, Activation, and the Sequential Unfolding of Natal Promise.txt",
    "The Inseparable Bond_ Medical Astrology's Integration of Celestial Cause and Physical Pathology.txt",
    "Astrology Research and Analysis (1).txt",
    "Improving Natal Chart Interpretation Guide (1).txt",
    "# PART 8 EXTENDED_ UNIVERSAL CAUSATION AUDIT FOR DECEMBER 2025.txt",
    "Astrological Hierarchies of Causation.txt",
    "Traditional Time-Lord Systems Research (1).txt",
    "Untitled document.txt",
    "The_Traditional_Astrologers_Complete_Reference.txt",
    "Refining Astrological Research Prompt.txt"
)

$output = "The_Complete_Astrology_Codex.txt"
Remove-Item $output -ErrorAction SilentlyContinue

foreach ($file in $files) {
    if (Test-Path $file) {
        Add-Content $output "`r`n================================================================================"
        Add-Content $output "START OF FILE: $file"
        Add-Content $output "================================================================================`r`n"
        Get-Content $file -Raw | Add-Content $output
    } else {
        Write-Host "Warning: File not found - $file"
    }
}

Write-Host "Merge completed. Output saved to $output"
