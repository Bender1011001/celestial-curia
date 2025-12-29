# Chapter 20: Synastry, Elections, and Planetary Joys

## Refining Deterministic Astrology for Computational Implementation

This chapter addresses three remaining refinement gaps in deterministic astrological software:

1. **Synastry Overlay Mechanics** — The mathematical relationships between one person's Almuten and another person's Hyleg
2. **Electional Protocols** — Step-by-step selection algorithms for optimal timing
3. **Planetary Joy Quantification** — Strength multipliers for accidental dignity calculations

---

## I. Synastry Overlay Mechanics: The Almuten-to-Hyleg Bridge

### Foundational Principle

When Person A's Almuten Figuris (most dignified planet) aspects or conjoins Person B's Hyleg (life-giving point), Person A's essential governing force directly influences the vitality and life direction of Person B.

### Computational Algorithm

**Step 1:** Calculate both charts completely:
- Person A's Almuten via point-scoring system
- Person B's Hyleg via hierarchical protocol (Sun/Moon in angles → Ascendant → Part of Fortune)

**Step 2:** Assess the aspect relationship:

| Aspect | Base Value |
|--------|------------|
| Conjunction | +5 |
| Trine/Sextile | +3 |
| No aspect | 0 |
| Square | -2 |
| Opposition | -1 |

**Step 3:** Apply modifiers:

```
Almuten-Hyleg Strength = 
    Aspect_Value
  + (Almuten_Dignity_Score ÷ 10)      [yields 0 to +2.5]
  + Almuten_House_Modifier            [angular +2, succedent +1, cadent -1]
  + Hyleg_House_Modifier              [angular +2, succedent +1, cadent -1]
  + Reception_Bonus                   [+1.5 if Almuten in Hyleg's sign dignity]
```

**Final Range:** -2 to +14 (scale to 0-100 for presentation)

### Asymmetry Recognition

The software must calculate **both directions**:
- Person A's Almuten → Person B's Hyleg (A vitalizes B)
- Person B's Almuten → Person A's Hyleg (B vitalizes A)

Present these separately to reveal power dynamics.

### Hierarchical Filtering

Flag when either Hyleg is weak (determined only after Sun/Moon failed to qualify). The Almuten-Hyleg interaction carries greatest weight when both are strongly established.

---

## II. Electional Protocols: The Selection Algorithm

### Input Parameters Required

1. **Statement of Intent** — Clear one-sentence description (e.g., "Begin a new business")
2. **Time Window** — Specific dates and hours available
3. **External Constraints** — Appointments, legal requirements, personal obligations

### The Twelve-Step Selection Algorithm

#### Step 1: Establish Significators

| Event Type | Primary Significator | Master Significators |
|------------|---------------------|---------------------|
| Business launch | 10th house ruler, Sun | Ascendant ruler, Moon |
| Marriage | 7th house ruler, Venus | Ascendant ruler, Moon |
| Medical procedure | 6th house ruler | Ascendant ruler, Moon |
| Legal action | 9th house ruler, Jupiter | Ascendant ruler, Moon |

#### Step 2: Filter by Lunar Phase

| Event Type | Preferred Phase |
|------------|-----------------|
| Growth, initiation, establishment | Waxing (New → Full) |
| Completion, release, dissolution | Waning (Full → New) |

#### Step 3: Eliminate Void-of-Course Moon

Calculate when Moon perfects its last major aspect before leaving its sign. Eliminate these periods (typically 2-6 hours/day).

#### Step 4: Check Retrograde Status

| Event Type | Avoid Retrograde |
|------------|-----------------|
| Contracts, communication | Mercury |
| Relationships, finances | Venus |
| Action, competition | Mars |

#### Step 5: Evaluate Significator Dignity

Identify times when primary significator occupies essential dignity (domicile, exaltation).

#### Step 6: Assess Angular Placement

Rank times when primary significator occupies angular houses (1st, 4th, 7th, 10th) higher.

#### Step 7: Examine Ascendant Aspects

| Configuration | Ranking |
|---------------|---------|
| Jupiter/Venus conjunct or sextile Ascendant | Optimal |
| No aspects to Ascendant | Neutral |
| Saturn/Mars square or conjunct Ascendant | Suboptimal |

#### Step 8: Evaluate Moon's Aspects to Significator

Moon applying to significator by trine/sextile/conjunction = Most favorable

#### Step 9: Check Sect Compatibility

- **Diurnal charts:** Jupiter and Mars above horizon preferred
- **Nocturnal charts:** Venus and Mars below horizon preferred

#### Step 10: Evaluate Part of Fortune

Ideally angular with well-placed, unafflicted ruler.

#### Step 11: Assess Luminary Dignities

Check Sun (day charts) or Moon (night charts) for essential dignity.

#### Step 12: Synthesize Composite Score

| Factor | Weight |
|--------|--------|
| Significator dignity | 20% |
| Ascendant ruler condition | 20% |
| Angular placements | 15% |
| Moon aspects | 15% |
| Benefic transits | 10% |
| Part of Fortune | 10% |
| Luminaries | 10% |

### Output Format

Present 3-5 optimal time windows ranked by composite score, with explanatory rationale for each.

---

## III. Planetary Joys: Quantified Accidental Dignity

### Traditional Joy Assignments

| Planet | House of Joy | Resonance |
|--------|--------------|-----------|
| Mercury | 1st | Self-expression, intellect |
| Moon | 3rd | Daily communication, movement |
| Venus | 5th | Pleasure, creativity, romance |
| Mars | 6th | Work, health, service |
| Sun | 9th | Spirituality, higher knowledge |
| Jupiter | 11th | Friends, groups, wishes |
| Saturn | 12th | Limitations, hidden matters |

### Quantification Protocol

**Primary Joy Modifier:** +2 points when planet occupies its house of joy

**Alternative Joy Modifier:** +1 point for mutual joy relationships:
- Jupiter in 9th (Sun's joy house)
- Saturn in 1st (Mercury's joy house)
- Mercury in 12th (Saturn's joy house)

**Hostile House Penalty:** -2 to -3 points when planet occupies house fundamentally opposed to its nature (e.g., Mars in 7th)

### Complete Strength Calculation Sequence

```
Total Strength = 
    Essential Dignity Score
  + Base House Accidental Dignity    [angular +4, succedent +2, cadent 0/-1]
  + Joy Modifier                     [+2 primary, +1 alternative]
  - Hostile House Penalty            [-2 to -3 if applicable]
  + Other Accidental Factors         [aspects, combustion, retrograde]
```

### Context-Specific Interpretation

| Chart Type | Joy Interpretation |
|------------|-------------------|
| Natal | Life area where native naturally excels |
| Electional | Strengthens event's connection to planet's domain |
| Horary | Matter proceeds smoothly along intended path |

---

## IV. Integration Framework

When analyzing relationships with elected timing, the software performs:

1. Calculate both individuals' complete natal charts (Almutenae, Hylegs)
2. Determine optimal electional moment based on event intention
3. Cast electional chart for optimal moment
4. Overlay electional chart onto both natal charts
5. Generate synastry analysis with Almuten-Hyleg strength values
6. Synthesize compatibility + timing assessment

### Output Structure

| Section | Content |
|---------|---------|
| 1. Natal Strengths | Each person's Almuten, Hyleg, key dignities |
| 2. Electional Chart | Optimized timing with significators and joys highlighted |
| 3. Synastry Overlays | Almuten-Hyleg interaction strengths (both directions) |
| 4. Synthesis | Relationship potential + timing appropriateness |

---

## Conclusion

These three refinements transform astrological software from interpretive art into deterministic computation where different practitioners analyzing the same data consistently generate identical results.

The unified computational architecture ensures:
- Synastry modules exchange standardized Almuten-Hyleg data
- Electional modules apply systematic filtering algorithms
- Joy modifiers contribute reproducible accidental dignity values
- All results are auditable yet concisely deterministic for practical use
