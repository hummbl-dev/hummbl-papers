# RQ-PEP-004: Peptide Stability and Degradation Pathways (Expanded Update)

**Research Question:** How do popular research peptides degrade, and what storage practices preserve potency?

**Date:** 2026-03-23 (expanded update of 2026-03-15 report)
**Status:** Complete
**Report ID:** RQ-PEP-004-v2

---

## Executive Summary

This report substantially expands on the March 15, 2026 stability survey by adding coverage of Ipamorelin and PT-141 (Bremelanotide), incorporating 2025 forced-degradation studies for semaglutide, detailing maleimide hydrolysis chemistry for the CJC-1295 DAC linker, and providing quantitative data on amber vial UV filtration, freeze-thaw losses, pH-dependent aggregation kinetics, and container-closure leachable risks. The core finding remains unchanged: lyophilized peptides in sealed vials with low residual moisture are remarkably robust, while reconstituted solutions are the fragile link in the chain. New data reinforces that pH management (keeping solutions at pH 7.0-7.8 for most peptides), nitrogen-purged headspace, and amber glass or foil wrapping are the three most impactful interventions beyond basic refrigeration.

---

## Table of Contents

1. [General Degradation Chemistry](#1-general-degradation-chemistry)
2. [BPC-157 Stability Profile](#2-bpc-157-stability-profile)
3. [Semaglutide Stability Profile](#3-semaglutide-stability-profile)
4. [TB-500 (Thymosin Beta-4) Stability Profile](#4-tb-500-thymosin-beta-4-stability-profile)
5. [CJC-1295 Stability Profile (With and Without DAC)](#5-cjc-1295-stability-profile-with-and-without-dac)
6. [Ipamorelin Stability Profile](#6-ipamorelin-stability-profile)
7. [PT-141 (Bremelanotide) Stability Profile](#7-pt-141-bremelanotide-stability-profile)
8. [Temperature Sensitivity Across Peptides](#8-temperature-sensitivity-across-peptides)
9. [Light Sensitivity and Photodegradation](#9-light-sensitivity-and-photodegradation)
10. [Reconstitution Stability](#10-reconstitution-stability)
11. [Storage Best Practices (Evidence-Based)](#11-storage-best-practices-evidence-based)
12. [Detection of Degradation](#12-detection-of-degradation)
13. [Master Comparison Table](#13-master-comparison-table)
14. [Sources](#14-sources)

---

## 1. General Degradation Chemistry

All peptides share a common set of chemical degradation pathways. Understanding these mechanisms is essential before examining peptide-specific profiles.

### 1.1 Hydrolysis

Water cleaves peptide bonds, fragmenting the chain. Aspartic acid (Asp) residues create peptide bonds approximately 100x more labile than other residues, making Asp-Xxx sequences kinetic hotspots for hydrolysis. The rate increases exponentially with temperature and is catalyzed by both acidic and basic conditions.

### 1.2 Oxidation

Susceptible residues include methionine (Met), cysteine (Cys), tryptophan (Trp), tyrosine (Tyr), and histidine (His). Oxidation is driven by dissolved oxygen, trace metal ions (Fe2+, Cu2+), peroxide contaminants, and light. Each needle puncture of a vial introduces headspace oxygen, creating cumulative oxidative stress over multi-dose use.

### 1.3 Deamidation

Asparagine (Asn) and glutamine (Gln) residues undergo deamidation to aspartic acid (Asp) and glutamic acid (Glu) respectively, introducing a negative charge that alters peptide function. The Asn-Gly sequence is the fastest-reacting "hotspot," with rates up to 70x faster than Asn followed by bulky residues. Deamidation is pH-dependent and accelerated at neutral-to-basic pH and elevated temperature.

### 1.4 Racemization

L-amino acids spontaneously convert to D-amino acids, particularly at Asp, Ser, and His residues. This alters receptor binding affinity and biological activity. Racemization products (D-Ser, D-His, D-Asp) have been specifically characterized in semaglutide forced-degradation studies.

### 1.5 Aggregation

Peptide molecules associate into dimers, oligomers, fibrils, and amorphous aggregates. Key drivers:

| Factor | Effect on Aggregation |
|--------|----------------------|
| Higher concentration | Accelerates aggregation |
| pH near isoelectric point | Maximizes aggregation (low net charge) |
| Higher ionic strength | Accelerates via Debye screening (~10x at high salt for IAPP peptide) |
| Higher temperature | Accelerates (but non-Arrhenius behavior is common) |
| Air-water interfaces | Act as hydrophobic surfaces promoting aggregation |
| Agitation/shaking | Introduces air bubbles, promotes surface denaturation |

Less than 5% deamidated impurity can trigger aggregation of otherwise pure peptide (demonstrated with amylin), highlighting the cascade effect of chemical degradation leading to physical instability.

### 1.6 Amino Acid Vulnerability Reference

| Amino Acid | Primary Vulnerability | Consequence |
|-----------|----------------------|-------------|
| Methionine (Met) | Oxidation to sulfoxide | Activity loss |
| Cysteine (Cys) | Oxidation, disulfide scrambling | Misfolding, aggregation |
| Tryptophan (Trp) | Photooxidation (absorbs <320 nm, epsilon=5500 M-1cm-1 at 280 nm) | Yellowing, kynurenine formation |
| Histidine (His) | Photo-oxidation, metal-catalyzed oxidation | Activity loss |
| Tyrosine (Tyr) | Photooxidation | Potency reduction |
| Asparagine (Asn) | Deamidation (especially Asn-Gly) | Charge change, altered function |
| Glutamine (Gln) | Deamidation (slower than Asn) | Charge change |
| Aspartic acid (Asp) | Isomerization, racemization, hydrolysis hotspot | Bond cleavage, altered structure |
| Serine (Ser) | Racemization | Altered stereochemistry |

---

## 2. BPC-157 Stability Profile

**Sequence:** Gly-Glu-Pro-Pro-Pro-Gly-Lys-Pro-Ala-Asp-Asp-Ala-Gly-Leu-Val (15 amino acids)

### 2.1 Key Structural Features

- **No methionine or cysteine residues**: BPC-157 is inherently resistant to the most common oxidation pathway (Met sulfoxide formation) and disulfide scrambling.
- **Asp10-Asp11 motif**: Two consecutive aspartic acid residues at positions 10-11 create a critical vulnerability. This Asp-Asp motif is the primary site for isomerization and drives deamidation/isomerization-related degradation in solution. This same motif makes synthesis challenging and creates solution-state instability.
- **High proline content**: Four prolines (positions 3, 4, 5, 8) constrain backbone flexibility and confer resistance to many proteases.
- **Gastric acid stability**: Unusually stable at pH 2-3 and resistant to pepsin digestion, enabling oral bioavailability. This derives from its origin as a fragment of a gastric protective protein (BPC).

### 2.2 Degradation Pathways (Ranked by Significance)

1. **Isomerization at Asp10-Asp11**: The dominant solution-phase degradation. Asp isomerizes to iso-Asp via a cyclic succinimide intermediate. This is pH- and temperature-dependent, accelerating above pH 6 and above 25C.
2. **Deamidation**: Glu2 can undergo slow deamidation. The Asp-Asp motif also facilitates deamidation-like rearrangements through succinimide formation.
3. **Hydrolysis**: Water cleaves peptide bonds, accelerated by heat. Primary route in reconstituted solutions over extended storage.
4. **Aggregation**: Occurs over time as degradation products accumulate, altering charge distribution and promoting intermolecular interactions.
5. **Photooxidation**: While BPC-157 lacks the most photosensitive residues (Met, Trp, Cys), the Leu and Val residues show minor susceptibility under prolonged UV exposure.

### 2.3 Stability Data

| Condition | Expected Stability | Confidence |
|-----------|-------------------|------------|
| Lyophilized at -20C | 2-3 years, minimal degradation | High (industry consensus) |
| Lyophilized at 2-8C | 12-18 months | High |
| Lyophilized at RT | Weeks to a few months | Moderate (vendor-dependent) |
| Reconstituted, BAC water, 2-8C | 4-6 weeks | High |
| Reconstituted, sterile water, 2-8C | 7-14 days | High |
| Reconstituted, frozen -20C | Months (avoid freeze-thaw) | Moderate |

### 2.4 Unique Consideration

BPC-157's Asp-Asp motif means that even high-purity starting material (>98% HPLC) will show detectable isomerization products within days of reconstitution at room temperature. Industry testing consensus places refrigerated reconstituted stability at 14-28 days for maintaining >95% purity by HPLC, with the Asp-Asp isomerization products being the first degradants to appear.

---

## 3. Semaglutide Stability Profile

**Structure:** 31-amino acid GLP-1 analog with C-18 fatty diacid chain attached at Lys26 via a mini-PEG spacer, plus Aib substitutions at positions 2 and 8.

### 3.1 Key Structural Features

- **C-18 fatty diacid modification**: Enables albumin binding (extending half-life to ~168 hours) but creates additional hydrophobic surface area that can drive aggregation.
- **Aib2, Aib8 substitutions**: Alpha-aminoisobutyric acid at positions 2 and 8 confers resistance to DPP-4 enzymatic cleavage.
- **Arg34 substitution**: Reduces susceptibility to certain endopeptidases.

### 3.2 Degradation Pathways

1. **Racemization**: D-amino acid isomers (D-Ser, D-His, D-Asp) are the best-characterized degradation products, identified by UPLC-HRMS in forced degradation studies. These reduce biological activity.
2. **Deamidation**: Asparagine and glutamine residues undergo deamidation, particularly at elevated pH.
3. **Oxidation**: Susceptible residues include His and Trp within the GLP-1 backbone.
4. **Aggregation/Fibrillation**: GLP-1 peptides are inherently prone to fibril formation. For GLP-1(7-37), a dramatic kinetic shift occurs between pH 7.5 and 8.2, with concentration-dependent nucleation-polymerization kinetics. Semaglutide is optimally stable at pH 7.4-7.8, where oligomer formation is prevented or delayed.
5. **Fatty acid chain degradation**: The C-18 fatty diacid undergoes sequential beta-oxidation in vivo. In storage, the acyl chain creates a hydrophobic domain that can promote intermolecular association.
6. **Truncation**: Shorter peptide fragments from bond cleavage at susceptible sites.

### 3.3 Forced Degradation Data (2025 Studies)

Two landmark 2025 preformulation studies (Malgave et al., Journal of Peptide Science; and a separate LC-HRMS study) provide quantitative degradation data:

| Condition | Duration | Key Finding |
|-----------|----------|-------------|
| Water, 25C | 24 hours | Minimal degradation |
| Water, 40C | 24 hours | Measurable degradation products |
| Water, 55C | 24 hours | Significant degradation |
| 80C | 3 hours | Semaglutide remained stable |
| 80C | 7 days | Extensive degradation |
| 25C, 40C, 60C | 28 days | Thermal stress profiling complete |
| pH 1.2, 25C/40C | 24 hours | Relatively stable |
| pH 7.4-7.8 | Optimal | Highest stability, prevents oligomer formation |
| pH <7.0 (with phenol) | -- | Stability decreases drastically |
| 40C/75% RH (ICH accelerated) | 6 months | Standard regulatory assessment |

### 3.4 Storage Specifications

**Pharmaceutical-grade (Ozempic/Wegovy pens):**
- Unopened: Refrigerate 2-8C, never freeze. Shelf life per manufacturer (typically 2 years).
- In-use: Refrigerated or RT up to 30C for up to 56 days. Cap on when not injecting.

**Compounded/lyophilized:**
- Lyophilized: -20C long-term, 2-8C short-term
- Reconstituted: 2-8C, use within 28 days

**Critical warning:** Semaglutide must NEVER be frozen. Freezing destroys the formulation's stability permanently, unlike most peptides where freezing is protective.

### 3.5 Humidity Sensitivity

Semaglutide is notably more humidity-sensitive than most peptides due to the acylated structure. High humidity (>70% RH) causes significant degradation within weeks for lyophilized forms. Oral semaglutide (Rybelsus) is specifically formulated for dry storage and does not require refrigeration but requires moisture protection as the primary concern.

---

## 4. TB-500 (Thymosin Beta-4) Stability Profile

**Structure:** TB-500 is the synthetic active fragment (amino acids 17-23) of full-length thymosin beta-4 (43 amino acids). TB-500 is a 7-amino acid acetylated peptide: Ac-LKKTET-OH (approximately). Full Tb4 contains the active sequence LKKTETQ.

### 4.1 Key Structural Features

- **N-terminal acetylation ("Ac-")**: Protects the N-terminus from aminopeptidase cleavage. This is a permanent covalent modification that significantly improves stability and bioavailability.
- **Lysine-rich sequence**: Multiple lysine residues contribute to water solubility but create potential sites for chemical modification.
- **No disulfide bonds**: Simplifies stability profile compared to cysteine-containing peptides.

### 4.2 Degradation Pathways

1. **C-terminal cleavage**: The primary fragmentation pathway. While the acetylated N-terminus is well protected, the C-terminus is vulnerable to serial exopeptidase cleavage, producing progressively shorter fragments.
2. **Oxidation**: Methionine residues in full-length Tb4 (particularly Met6) are oxidation-sensitive, forming methionine sulfoxide. TB-500 (the fragment) has reduced Met content but trace oxidation is still possible at other residues.
3. **Deamidation**: Glutamine and asparagine residues, particularly in the full-length Tb4 sequence, undergo deamidation. The threonine and glutamic acid in TB-500 are relatively stable.
4. **Aggregation**: Formation of dimers and oligomers through intermolecular interactions, particularly at higher concentrations.
5. **Hygroscopic absorption**: The lyophilized powder readily absorbs atmospheric moisture, which accelerates all degradation pathways. Moisture ingress is the primary threat to lyophilized TB-500.

### 4.3 Stability Data

| Condition | Expected Stability | Notes |
|-----------|-------------------|-------|
| Lyophilized at -20C | 24+ months, <5% degradation | Best option |
| Lyophilized at 2-8C | 12-18 months | Acceptable for active use |
| Lyophilized at RT | 3-6 months | Not recommended |
| Reconstituted, BAC water, 2-8C | 14-28 days (>95% purity) | Standard use window |
| Reconstituted at RT | 7-14 days | Accelerated C-terminal cleavage |

### 4.4 Freeze-Thaw Sensitivity

TB-500 shows measurable degradation with each freeze-thaw cycle, with estimates of 2-5% peptide content loss per cycle. This makes aliquoting into single-use portions before freezing a strongly recommended practice. The mechanism is thought to involve ice crystal formation disrupting peptide structure at the air-ice interface.

---

## 5. CJC-1295 Stability Profile (With and Without DAC)

### 5.1 CJC-1295 Without DAC (Mod GRF 1-29)

**Structure:** 29-amino acid modified GHRH fragment with four amino acid substitutions at positions 2, 8, 15, and 27 conferring DPP-4 resistance.

**Degradation pathways:**
1. **DPP-4 cleavage** (in vivo): The primary in-vivo degradation route, partially mitigated by the amino acid substitutions.
2. **Hydrolysis**: Standard peptide bond cleavage, particularly at Asp residues.
3. **Oxidation**: Met and Trp residues in the GHRH backbone are susceptible.
4. **Deamidation**: Asn residues undergo standard deamidation kinetics.
5. **Aggregation**: At higher concentrations, GHRH analogs can form oligomeric species.

### 5.2 CJC-1295 With DAC

**Additional structural element:** N-epsilon-3-maleimidopropionamide (MPA) attached via the Lys30 side chain. The maleimide group forms a covalent thioether bond with Cys34 on serum albumin after injection.

**DAC-specific degradation chemistry:**

The maleimide linker introduces unique stability considerations:

1. **Maleimide ring hydrolysis**: The thiosuccinimide linkage formed after albumin conjugation undergoes two competing reactions:
   - **Retro-Michael elimination**: Reversal of the thiol-maleimide bond, releasing the peptide from albumin (loss of extended half-life).
   - **Ring opening (hydrolysis)**: Conversion to the ring-opened maleamic acid derivative, which is resistant to the retro-Michael reaction and thus stabilizes the conjugate.

2. **pH-dependent hydrolysis**: Maleimide hydrolysis is first-order in hydroxide ion above pH ~5, meaning higher pH accelerates ring opening. At storage pH, the succinimide can interconvert between open and closed conformations; >15% conversion to closed form was observed at 25C after 6 months in liquid formulation.

3. **Pre-injection linker stability**: In lyophilized form, the maleimide group is relatively stable. In reconstituted solution, the reactive maleimide can undergo:
   - Hydrolysis to maleamic acid (loss of albumin-binding capacity)
   - Reaction with any free thiol-containing impurities in the diluent
   - Self-polymerization at high concentrations

### 5.3 Comparative Stability

| Property | CJC-1295 with DAC | CJC-1295 without DAC |
|----------|-------------------|---------------------|
| In vivo half-life | ~6-8 days (albumin-bound) | ~30 minutes |
| Lyophilized stability (-20C) | 2+ years | 2+ years |
| Reconstituted stability (2-8C) | 2-4 weeks | 2-4 weeks |
| DPP-4 resistance | High (DAC + substitutions) | Moderate (substitutions only) |
| Unique risk | Maleimide hydrolysis in solution | Standard degradation only |
| Reconstitution note | Must dissolve gently; maleimide is sensitive to agitation | Standard gentle reconstitution |

### 5.4 Reconstituted Blend Stability Warning

In blended reconstituted preparations (e.g., CJC-1295 + Ipamorelin), the two compounds may degrade at different rates. If one compound is significantly less stable than the other, the ratio shifts over time even if correct at manufacture. This is particularly relevant because CJC-1295/Ipamorelin blends are among the most popular peptide stacks.

---

## 6. Ipamorelin Stability Profile

**Sequence:** Aib-His-D-2-Nal-D-Phe-Lys-NH2 (pentapeptide, MW ~711.9 Da)

### 6.1 Key Structural Features

- **Aminoisobutyric acid (Aib) N-terminus**: The alpha,alpha-disubstituted amino acid constrains backbone geometry and strongly resists aminopeptidase cleavage.
- **Two D-amino acids**: D-2-naphthylalanine (D-2-Nal) at position 3 and D-phenylalanine (D-Phe) at position 4 confer proteolytic stability. D-amino acids are not recognized by most proteases.
- **C-terminal amidation (-NH2)**: Protects against carboxypeptidase cleavage.
- **Small size**: At only 5 amino acids, ipamorelin has fewer potential degradation sites than larger peptides.

### 6.2 Degradation Pathways

1. **Histidine oxidation**: His2 is the most oxidation-vulnerable residue. Metal-catalyzed oxidation (particularly by trace Fe2+ or Cu2+) targets the imidazole ring, producing 2-oxo-histidine. This is the primary chemical degradation pathway.
2. **Racemization**: While ipamorelin intentionally contains D-amino acids, the L-amino acid residues (particularly His) can racemize. Racemized D-amino acid variants have been identified as impurities in testing.
3. **Deletion peptides**: Synthesis-related impurities (des-Aib, des-Lys variants) may be present in lower-quality preparations and can increase over time via hydrolysis.
4. **Oxidation artifacts**: Identified in falsified products, indicating either poor manufacturing or storage-related oxidation.
5. **Aggregation**: Less prone than larger peptides due to small size, but possible at very high concentrations.

### 6.3 Stability Data

| Condition | Expected Stability | Notes |
|-----------|-------------------|-------|
| Lyophilized at -20C | 24+ months | Excellent stability |
| Lyophilized at 2-8C | 12+ months | Good |
| Lyophilized at RT | Stable ~3 weeks (ProSpec data) | Short-term acceptable |
| Reconstituted, 2-8C | 2-7 days (without carrier protein) | Short window without stabilizer |
| Reconstituted, 2-8C (BAC water) | Up to 30 days | With preservative |
| Reconstituted, frozen -20C | Months | Add 0.1% BSA/HSA for long-term |

### 6.4 Enhanced Stability Features

Ipamorelin is notably more proteolytically stable than most peptides in its class due to the triple protection of Aib N-terminus, dual D-amino acids, and C-terminal amidation. However, chemical degradation (oxidation of His, hydrolysis) still occurs in solution, making proper storage essential. The small size means degradation of even one residue eliminates biological activity.

---

## 7. PT-141 (Bremelanotide) Stability Profile

**Sequence:** Ac-Nle-c[Asp-His-D-Phe-Arg-Trp-Lys]-NH2 (cyclic heptapeptide with lactam bridge)

### 7.1 Key Structural Features

- **Cyclic structure**: Lactam bridge between Asp and Lys side chains constrains the peptide into a ring, dramatically increasing proteolytic stability compared to linear alpha-MSH analogs.
- **Norleucine (Nle) at position 4**: Replaces the oxidation-sensitive methionine (Met4) of native alpha-MSH. This deliberate substitution eliminates the most common oxidation vulnerability.
- **D-Phenylalanine (D-Phe)**: Confers resistance to enzymatic degradation at that position.
- **Tryptophan (Trp)**: The indole side chain absorbs UV light strongly (epsilon = 5500 M-1cm-1 at 280 nm) and is the primary photodegradation target.
- **Histidine (His)**: Susceptible to metal-catalyzed oxidation and photooxidation.

### 7.2 Degradation Pathways

1. **Tryptophan photooxidation**: The dominant degradation pathway under light exposure. Trp is oxidized to kynurenine, N-formylkynurenine, and hydroxytryptophan, producing visible yellow-brown chromophores. This occurs under both UV (<320 nm) and, to a lesser extent, visible light via photosensitized mechanisms involving dissolved oxygen.
2. **Histidine oxidation**: Metal-catalyzed and photooxidation of the imidazole ring produces 2-oxo-histidine.
3. **Lactam bridge hydrolysis**: Under acidic conditions or extended storage, the lactam bridge can hydrolyze, converting the cyclic peptide to a linear form with dramatically reduced activity and stability.
4. **Arginine modification**: Arg can undergo reaction with carbonyl compounds (Maillard-type reactions) if glucose or reducing sugars are present in the formulation.
5. **Deamidation**: Asp within the ring can undergo isomerization via the succinimide intermediate.

### 7.3 Light Sensitivity (Critical)

PT-141 is among the most light-sensitive peptides in common use due to its tryptophan residue within the constrained cyclic structure:

- **UV-B (280-315 nm)**: Rapid degradation. Direct absorption by Trp indole ring.
- **UV-A (315-400 nm)**: Moderate degradation via photosensitized oxidation.
- **Visible light (400-500 nm)**: Slow but measurable degradation, particularly in the presence of dissolved oxygen.
- **Amber vial protection**: Essential. Pharmaceutical-grade amber glass blocks ~90% of UV-B and ~70% of UV-A, providing substantial but not complete protection.
- **Practical consequence**: PT-141 vials should never be left on a counter under room lighting. Even brief repeated exposure during daily use accumulates over weeks.

### 7.4 Stability Data

| Condition | Expected Stability | Notes |
|-----------|-------------------|-------|
| Lyophilized, desiccated, below -18C | 2+ years | Best option |
| Lyophilized at RT | ~3 weeks (ProSpec data) | Very limited |
| Reconstituted, 4C | 2-7 days (without carrier protein) | Short window |
| Reconstituted, 4C (BAC water, dark) | Up to 30 days | Must protect from light |
| Reconstituted, frozen -18C | Months | Add 0.1% BSA/HSA; avoid freeze-thaw |

### 7.5 Practical Guidance

- Always use amber vials or wrap clear vials in aluminum foil.
- Minimize the number and duration of light exposures during dose preparation.
- The Nle-for-Met substitution means PT-141 resists the most common peptide oxidation pathway, but Trp and His create alternative oxidation vulnerabilities that require light protection.
- A half-life of ~120 minutes in vivo (due to the cyclic structure) is far longer than linear analogs.

---

## 8. Temperature Sensitivity Across Peptides

### 8.1 Comprehensive Temperature Stability Matrix

| Peptide | Lyophilized -20C | Lyophilized 2-8C | Lyophilized RT | Reconstituted 2-8C (BAC) | Reconstituted RT |
|---------|------------------|-------------------|----------------|---------------------------|-------------------|
| **BPC-157** | 2-3 years | 12-18 months | Weeks-months | 4-6 weeks | Days (rapid Asp isomerization) |
| **Semaglutide** | 2+ years | 2 years (mfr) | Not recommended | 28-56 days | Up to 56 days (pen, <30C) |
| **TB-500** | 24+ months | 12-18 months | 3-6 months | 14-28 days | 7-14 days |
| **CJC-1295 (DAC)** | 2+ years | 12-18 months | Weeks | 2-4 weeks | Not recommended |
| **CJC-1295 (no DAC)** | 2+ years | 12-18 months | Weeks | 2-4 weeks | Not recommended |
| **Ipamorelin** | 24+ months | 12+ months | ~3 weeks | Up to 30 days | Days |
| **PT-141** | 2+ years | 12+ months | ~3 weeks | Up to 30 days (dark) | Not recommended |

### 8.2 Accelerated Stability (40C/75% RH, ICH Q1A(R2))

The ICH Q1A(R2) guideline defines accelerated stability testing at 40C +/- 2C and 75% RH +/- 5% RH for 6 months. This condition simulates approximately 2 years of real-time storage at 25C/60% RH.

- **Semaglutide**: 2025 forced-degradation studies show measurable degradation products at 40C within 24 hours in water, with significant degradation at 28 days. Remains stable for 3 hours at 80C. Stability decreases drastically below pH 7.0 in the presence of phenol.
- **Bacitracin (peptide antibiotic, model compound)**: Accelerated stability predictions at 40C/75% RH validated against long-term data at 30C/53% RH, confirming Arrhenius-based shelf-life predictions for peptides under ICH conditions.
- **General peptide rule**: For lyophilized peptides, moisture control is more impactful than temperature at the 40C/75% RH condition. A vial with compromised seal at 70% humidity for 24 hours experiences more degradation than an intact vial at 45C for 48 hours.

### 8.3 Freeze-Thaw Effects

| Peptide | Estimated Loss Per Cycle | Mechanism | Recommendation |
|---------|-------------------------|-----------|----------------|
| TB-500 | 2-5% per cycle | Ice crystal disruption, air-ice interface denaturation | Aliquot before freezing |
| BPC-157 | 1-3% per cycle (estimated) | Concentration effects at ice boundaries | Aliquot before freezing |
| Semaglutide | **Do not freeze** | Irreversible formulation damage | Never freeze pens; lyophilized ok |
| CJC-1295 | 2-5% per cycle (estimated) | Standard freeze-thaw denaturation | Aliquot before freezing |
| Ipamorelin | Moderate (not quantified) | Standard mechanisms | Add carrier protein for frozen storage |
| PT-141 | Moderate (not quantified) | Standard mechanisms | Add 0.1% BSA/HSA; aliquot |

**General finding**: In a mass spectrometry-based study, 29 of the detected peptides showed stable peak areas across 1 and 10 freeze-thaw cycles, but peptides were categorized as "stable" (<5% loss), "slow decay" (5-50% loss), or "fast decay" (>50% loss), indicating highly peptide-specific responses. The safest universal practice is to aliquot into single-use volumes before freezing.

### 8.4 Reconstituted Peptide Longevity at Each Temperature

| Temperature | Maximum Recommended Use Window | Condition |
|-------------|-------------------------------|-----------|
| Room temperature (20-25C) | 7 days maximum for any peptide | Emergency only |
| Refrigerated (2-8C) | Robust peptides: 60 days; Standard: 45 days; GLP-1 analogs: 22 days; Volatile compounds: 5 days | Standard storage |
| Frozen (-20C) | Months (single-use aliquots only) | Long-term reconstituted storage |

---

## 9. Light Sensitivity and Photodegradation

### 9.1 Photosensitivity Ranking

| Peptide | Light Sensitivity | Primary Photosensitive Residue(s) | Risk Level |
|---------|-------------------|-----------------------------------|------------|
| **PT-141** | HIGH | Trp (strong UV absorber), His | Critical -- always protect |
| **BPC-157** | MODERATE | Glu, minor aromatic contribution | Important |
| **Semaglutide** | MODERATE | His, Trp in GLP-1 backbone | Important |
| **Ipamorelin** | MODERATE | His, 2-Nal (naphthyl absorber) | Important |
| **TB-500** | LOW-MODERATE | Limited aromatic content | Standard precautions |
| **CJC-1295** | LOW-MODERATE | Standard GHRH residues | Standard precautions |

### 9.2 Photodegradation Mechanisms

**UV-B (280-315 nm):** Direct absorption by aromatic amino acids. Tryptophan absorbs most strongly (epsilon = 5500 M-1cm-1 at 280 nm). Tyrosine and phenylalanine also absorb in this range. This triggers direct bond cleavage and radical formation.

**UV-A (315-400 nm):** Indirect photosensitized oxidation. Aromatic residues absorb and transfer energy to dissolved oxygen, generating singlet oxygen (1O2) and superoxide, which then attack susceptible residues.

**Visible light (400-800 nm):** A 2023 study (PMC9926095) confirmed that visible light exposure leads to photooxidation of protein formulations through formation of reactive oxygen species (ROS). The mechanism involves trace photosensitizers (flavins, porphyrins) in solution. The impact depends significantly on protein concentration and dissolved oxygen.

**Headspace oxygen effect:** Photooxidation depends significantly on oxygen in the vial headspace. Nitrogen-purged headspace dramatically reduces photo-induced degradation even under light exposure.

### 9.3 Amber Vial Effectiveness

Quantitative UV/visible light transmission data for pharmaceutical-grade amber glass:

| Wavelength Range | Amber Glass Filtration | Significance |
|-----------------|----------------------|--------------|
| UV-B (280-315 nm) | ~90% blocked | Major protection for Trp/Tyr/Phe |
| UV-A (315-400 nm) | ~70% blocked | Good but incomplete |
| Visible (400-450 nm, HEV) | ~0-30% blocked (standard); up to 99.8% (premium 400nm cutoff) | Variable by glass quality |
| Visible (>450 nm) | ~0% blocked | Minimal protection |

**Practical effectiveness data:** In one study, 78% of peptide serums in clear glass lost 40% of active peptide concentration after 8 weeks under ambient indoor lighting, while the same formulation in amber glass retained 92% potency under identical conditions.

**Bottom line:** Amber glass provides strong UV protection but limited visible light protection. For the most photosensitive peptides (PT-141, any Trp-containing peptide), amber glass plus storage in a dark location (drawer, box, refrigerator) is recommended.

---

## 10. Reconstitution Stability

### 10.1 Bacteriostatic Water vs. Sterile Water

| Parameter | Bacteriostatic Water (BAC) | Sterile Water for Injection |
|-----------|---------------------------|----------------------------|
| Preservative | 0.9% benzyl alcohol | None |
| Multi-dose use | Yes (28 days per USP) | No -- single use only |
| Microbial inhibition | Bacteriostatic (inhibits growth) | None |
| Peptide stability | 4-6 weeks refrigerated (most peptides) | 7-14 days refrigerated |
| Reconstituted vial life | 28 days (BAC water vial after first puncture) | Discard unused portion |
| Cost | Higher (~$5-15 per 30mL vial) | Lower (~$1-5) |
| Benzyl alcohol sensitivity | Contraindicated in neonates; rare adult sensitivity | No concerns |

**Key difference:** Without preservatives, peptides reconstituted with sterile water degrade more rapidly due to microbial contamination risk. Bacteria metabolize the peptide as a nutrient source and introduce pyrogens. BAC water's benzyl alcohol inhibits microbial growth, extending usable life to 4-6 weeks for most peptides.

### 10.2 Benzyl Alcohol Concentration Effects

The standard 0.9% (w/v) benzyl alcohol concentration in BAC water is:
- **Antimicrobially effective** against most bacteria and fungi at this concentration
- **Generally compatible** with peptide stability at 0.9%
- **Potentially destabilizing** at higher concentrations (>2%) for some peptides, as benzyl alcohol can interact with hydrophobic peptide regions and promote aggregation
- **pH effect**: BAC water is typically pH 4.5-7.0, which is acceptable for most peptide reconstitution

### 10.3 pH Effects on Reconstituted Stability

| pH Range | Effect on Stability | Best For |
|----------|--------------------|---------|
| pH 2-3 | Minimizes deamidation; increases hydrolysis risk | BPC-157 (uniquely stable here) |
| pH 4-5 | Good balance; reduced deamidation and aggregation | Hydrophobic peptides, acidic reconstitution |
| pH 5-6 | Moderate stability for most peptides | General use |
| pH 7.0-7.8 | Optimal for semaglutide; higher deamidation risk for Asn-containing peptides | GLP-1 analogs |
| pH >8 | Accelerated deamidation, aggregation, and racemization | Avoid for storage |

**Key principle:** Formulation pH should be far from the isoelectric point of the peptide to maintain high net charge and electrostatic repulsion, preventing aggregation. For peptides with Asn-Gly sequences, slightly acidic pH (4-6) substantially slows deamidation.

### 10.4 Concentration Effects on Aggregation

| Concentration | Aggregation Risk | Practical Guidance |
|---------------|-----------------|-------------------|
| <0.5 mg/mL | Low | Standard use, minimal aggregation concern |
| 0.5-2.0 mg/mL | Moderate | Monitor for turbidity; typical reconstitution range |
| 2.0-5.0 mg/mL | Elevated | GLP-1 peptides shift from spherulite to fibril morphology above ~5 mg/mL |
| >5.0 mg/mL | High | Gel-like aggregates possible; not recommended for storage |

Higher peptide concentration accelerates aggregation across multiple systems, following nucleation-polymerization kinetics. At typical consumer reconstitution concentrations (1-3 mg/mL), aggregation is manageable with proper refrigeration and limited storage duration.

### 10.5 Alternative Reconstitution Solvents

| Solvent | Use Case | Notes |
|---------|----------|-------|
| BAC water (0.9% benzyl alcohol) | Standard multi-dose reconstitution | Gold standard for consumer use |
| Sterile water for injection | Single-use only | Discard after one use |
| PBS (phosphate buffered saline) | Research/laboratory use | pH-buffered (7.4); good for cell assays |
| Normal saline (0.9% NaCl) | Clinical injection | Isotonic; no preservative |
| 5% acetic acid in water | Hydrophobic or basic peptides (Arg/Lys-rich) | Aids dissolution; not for all peptides |

---

## 11. Storage Best Practices (Evidence-Based)

### 11.1 Lyophilized Storage Guidelines

| Guideline | Evidence Basis | Citation Context |
|-----------|---------------|-----------------|
| Store at -20C to -80C for >6 months | Industry consensus; ICH Q1A(R2) accelerated data validates long-term stability | Bachem, GenScript, Sigma-Aldrich guidelines |
| -80C preferred for >1 year | Arrhenius kinetics predict ~4x slower degradation vs -20C | General thermodynamic principle |
| 2-8C acceptable for <6 months active use | Multiple vendor stability studies show <5% degradation | Verified Peptides, Creative Peptides data |
| Include desiccant packets | Moisture is more destructive than moderate temperature excursions for sealed lyophilized peptides | GenScript, Sigma-Aldrich handling guides |
| Verify crimp cap integrity | Compromised seals allow moisture ingress within hours | JPT, Bachem guidelines |
| Allow vials to warm to RT before opening | Prevents moisture condensation on cold powder surface | Universal recommendation |

### 11.2 Reconstituted Storage Guidelines

| Guideline | Evidence Basis |
|-----------|---------------|
| Refrigerate immediately after reconstitution (2-8C) | All degradation pathways accelerate above 8C |
| Use BAC water for multi-dose vials | 28-day USP multi-dose preservative standard |
| Inject diluent slowly down vial wall | Prevents foaming; agitation promotes aggregation |
| Swirl gently, never shake | Shaking creates air-water interfaces that denature peptides |
| Label with reconstitution date | Critical for tracking 4-6 week use window |
| Use within 4-6 weeks (BAC water) or 7-14 days (sterile water) | Aggregate industry data; peptide-specific windows vary |
| Minimize needle punctures | Each puncture introduces oxygen and contamination risk |
| Wipe septum with alcohol swab before each draw | Reduces microbial contamination risk |

### 11.3 Container-Closure Considerations

**Glass type matters:**
- **Type I borosilicate glass** (clear or amber): Gold standard for pharmaceutical peptide storage. Low extractables, chemically inert, USP-compliant.
- **Type II soda-lime glass**: Acceptable but higher alkali leaching, particularly at elevated pH.
- **Plastic (polypropylene)**: Acceptable for short-term storage. Risk of peptide adsorption to hydrophobic surfaces, reducing effective concentration. Not recommended for long-term storage.

**Rubber stopper leachables:**
- Butyl or halogenated butyl elastomer stoppers are standard for lyophilized products (low gas permeation, low moisture absorption, good sealing).
- Fluoropolymer-coated stoppers minimize extractable/leachable chemicals from rubber into the peptide.
- For lyophilized products, leachables primarily migrate via **outgassing**: volatile and semi-volatile organic compounds from the rubber migrate into the vial headspace and adsorb onto the dry lyophilized cake. The extreme dryness and high surface area of the cake exacerbate absorption.
- A 2022 PDA study recommends single time point leachables testing at the 1-year mark for lyophilized products in rubber-stoppered glass vials, as this allows sufficient time for chemical migration.
- **Practical consumer note:** Pharmaceutical-grade crimp-sealed vials with fluoropolymer-coated stoppers are vastly superior to screw-cap vials with uncoated rubber. This is a meaningful quality indicator when evaluating peptide vendors.

### 11.4 Practical Consumer Storage Guide

**On arrival:**
1. Inspect packaging for damage, crushed boxes, torn seals
2. Verify crimp cap integrity (should be flush, no looseness)
3. Check powder appearance: white to off-white fluffy powder or compact cake; any liquid in a lyophilized vial = failure
4. Transfer to -20C freezer within 30 minutes

**Before reconstitution:**
1. Allow vial to reach room temperature (15-30 minutes) before opening -- prevents moisture condensation on cold powder
2. Prepare BAC water, alcohol swabs, and insulin syringes
3. Clean hands and work surface

**During reconstitution:**
1. Inject BAC water slowly down the inside wall of the vial
2. Never squirt directly onto powder
3. Swirl very gently; never shake
4. Allow 5-10 minutes for complete dissolution
5. Solution should be clear and colorless (see Section 12 for exceptions)

**After reconstitution:**
1. Label vial with: peptide name, concentration, reconstitution date, discard date
2. Refrigerate immediately at 2-8C
3. Store in amber vial or wrap in aluminum foil
4. Store in back of refrigerator (more stable temperature than door)
5. Wipe septum with alcohol swab before each draw
6. Discard after 4-6 weeks (BAC water) or 7-14 days (sterile water)

---

## 12. Detection of Degradation

### 12.1 Visual Indicators

| Sign | Meaning | Action |
|------|---------|--------|
| **Crystal clear, colorless** | Normal | Use |
| **Slight cloudiness** | Possible cold precipitation or early aggregation | Allow 30 minutes at RT; if clears, likely ok; if persists, discard |
| **Persistent milky cloudiness** | Protein aggregation or bacterial growth | Discard |
| **Yellowing** | Tryptophan/tyrosine oxidation (kynurenine chromophores) | Discard -- irreversible |
| **Brown/dark discoloration** | Severe oxidation or microbial contamination | Discard immediately |
| **Visible particles or "snow globe" effect** | Aggregation or precipitation | Discard |
| **Gel-like or syrupy consistency** | Advanced aggregation | Discard |
| **Visible crystals (glass-like)** | Peptide precipitation | Discard |
| **Foam that persists >5 minutes** | Possible denaturation | Investigate |
| **Wet or clumped lyophilized powder** | Moisture ingress through compromised seal | Do not reconstitute -- likely degraded |
| **Powder color change from white** | Oxidation or chemical degradation | Suspect degradation |

**Peptide-specific normal appearances:**

| Peptide | Normal Reconstituted Appearance | Abnormal Signs |
|---------|-------------------------------|----------------|
| BPC-157 | Crystal clear, colorless | Any cloudiness |
| Semaglutide | Crystal clear; slight viscosity normal | White clouds, strings, gel formation |
| TB-500 | Crystal clear, colorless | Any cloudiness or particles |
| CJC-1295 | Crystal clear, colorless | Any cloudiness |
| Ipamorelin | Crystal clear, colorless | Any cloudiness or yellowing |
| PT-141 | Crystal clear, colorless | Yellow tint = Trp oxidation |

### 12.2 Practical Field Test for Cloudiness

For reconstituted solutions that develop cloudiness:
1. Hold sealed vial under warm (not hot) running water for 20 seconds
2. Gently invert 5 times
3. If cloudiness dissipates uniformly: likely cold precipitation (physical, not chemical) -- may be acceptable
4. If cloudiness persists: discard (indicates aggregation or microbial contamination)

### 12.3 Analytical Methods for Detecting Degradation

| Method | What It Detects | Cost | Consumer Accessible? |
|--------|----------------|------|---------------------|
| **RP-HPLC** | Purity percentage, degradation product peaks | $50-200 per sample | No (requires lab) |
| **LC-MS/HRMS** | Molecular identity, specific degradation products, D-amino acid isomers | $100-500 per sample | No |
| **MALDI-TOF MS** | Molecular weight confirmation, fragmentation | $50-150 | No |
| **Circular Dichroism (CD)** | Secondary structure changes, unfolding | $100-300 | No |
| **FTIR spectroscopy** | Aggregation (beta-sheet formation) | $50-200 | No |
| **Raman spectroscopy** | Molecular fingerprinting, structural changes | $50-200 | Emerging (portable devices) |
| **UV-Vis spectrophotometry** | Concentration, Trp oxidation products | $10-50 | Potentially (simple spectrophotometers) |
| **Visual inspection** | Turbidity, color, particles | Free | Yes |

### 12.4 Can Consumers Detect Degradation Without Lab Equipment?

**What consumers CAN detect:**
- Visible turbidity, color changes, particles, gel formation (see 12.1)
- Wet or discolored lyophilized powder
- Compromised vial seals
- Diminished subjective effects compared to fresh preparation

**What consumers CANNOT detect:**
- Early-stage chemical degradation (<5-10% loss) -- no visual signs
- Racemization products (look identical in solution)
- Deamidation products (often clear and colorless)
- Low-level microbial contamination (below visible turbidity threshold)
- Specific impurity profiles (requires HPLC/MS)
- Endotoxin/pyrogen contamination (requires LAL assay)

**Practical reality:** By the time degradation is visually apparent, the peptide has typically lost substantial potency. Visual inspection is a necessary but insufficient quality check. The most reliable consumer strategy combines:
1. Visual inspection at every use
2. Strict adherence to storage timelines
3. Purchase from vendors providing lot-specific Certificates of Analysis with HPLC and MS data
4. Third-party testing services (Janoshik, ACS Lab Testing) for independent verification

### 12.5 When to Suspect Degradation Without Visual Signs

- Reconstituted for longer than 4-6 weeks
- Known temperature excursion (left out overnight, shipping delay)
- Vial seal appeared compromised on arrival
- Effects seem diminished compared to fresh preparation from same vendor
- Multiple freeze-thaw cycles have occurred
- Vial has been exposed to light repeatedly

---

## 13. Master Comparison Table

| Property | BPC-157 | Semaglutide | TB-500 | CJC-1295 (DAC) | CJC-1295 (no DAC) | Ipamorelin | PT-141 |
|----------|---------|-------------|--------|----------------|-------------------|------------|--------|
| **Size** | 15 aa | 31 aa + C18 acyl | 7 aa (fragment) | 29 aa + DAC | 29 aa | 5 aa | 7 aa (cyclic) |
| **Lyophilized -20C** | 2-3 yr | 2+ yr | 2+ yr | 2+ yr | 2+ yr | 2+ yr | 2+ yr |
| **Reconstituted 2-8C (BAC)** | 4-6 wk | 28-56 d | 14-28 d | 2-4 wk | 2-4 wk | Up to 30 d | Up to 30 d (dark) |
| **Primary degradation** | Asp-Asp isomerization | Racemization, fibrillation | C-terminal cleavage | Maleimide hydrolysis | DPP-4 (in vivo) | His oxidation | Trp photooxidation |
| **Light sensitivity** | Moderate | Moderate | Low | Low | Low | Moderate | HIGH |
| **Freeze tolerance** | Yes (lyoph) | NEVER freeze pens | Yes (lyoph) | Yes (lyoph) | Yes (lyoph) | Yes (lyoph) | Yes (lyoph) |
| **Freeze-thaw loss** | 1-3%/cycle | N/A (no freeze) | 2-5%/cycle | 2-5%/cycle | 2-5%/cycle | Moderate | Moderate |
| **Humidity sensitivity** | Moderate | HIGH | HIGH (hygroscopic) | Moderate | Moderate | Moderate | Moderate |
| **Unique feature** | Gastric acid stable | Never freeze; pH 7.4-7.8 optimal | N-terminal acetylation | Maleimide linker | DPP-4 resistant subs | Triple protease protection | Cyclic + Nle-for-Met |
| **Key vulnerability** | Asp10-Asp11 motif | Humidity, fibrillation | Moisture ingress | Maleimide ring chemistry | Standard hydrolysis | His oxidation | Trp + light |
| **Optimal storage pH** | 4-6 (stable even at pH 2-3) | 7.4-7.8 | 5-7 | 5-7 | 5-7 | 5-7 | 5-7 |

---

## 14. Sources

### Peer-Reviewed Literature

- Malgave et al. (2025). "Influence of Buffering Capacity, pH, and Temperature on the Stability of Semaglutide: A Preformulation Study." *Journal of Peptide Science*. [Wiley](https://onlinelibrary.wiley.com/doi/10.1002/psc.70039)
- LC-HRMS Preformulation Study (2025). "Effect of pH, buffers, molarity, and temperature on solution state degradation of semaglutide using LC-HRMS." [PubMed](https://pubmed.ncbi.nlm.nih.gov/40490042/)
- D-amino acid characterization in semaglutide. "Characterization of low-level D-amino acid isomeric impurities of Semaglutide using LC-HRMS." [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0731708522005854)
- Cetrorelix racemization/deamidation study (2025). "LC-QTOF Characterization of Racemization and Deamidation Impurities in Cetrorelix Acetate." [Springer](https://link.springer.com/article/10.1007/s10989-025-10773-4)
- Peptide aggregation review (2017). "Factors affecting the physical stability (aggregation) of peptide therapeutics." *Interface Focus*. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5665799/)
- Formulation strategies for peptide stability (2023). "Designing Formulation Strategies for Enhanced Stability of Therapeutic Peptides in Aqueous Solutions." *Pharmaceutics*. [MDPI](https://www.mdpi.com/1999-4923/15/3/935)
- Protein photodegradation in visible range (2023). [PMC](https://ncbi.nlm.nih.gov/pmc/articles/PMC9926095)
- Photo-oxidation of therapeutic proteins (2022). [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8779573/)
- Photodegradation of Trp/Cys cyclic peptides: octreotide and somatostatin. [ACS](https://pubs.acs.org/doi/10.1021/mp5003174)
- E&L in lyophilized products. "Recommendation of Single Time Point Leachables Testing for Lyophilized Biotechnology Products." [PubMed](https://pubmed.ncbi.nlm.nih.gov/35257694/)
- Practical lyophilized drug product development (2025). [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11744310/)
- Maleimide-thiol conjugate stability. "Long-Term Stabilization of Maleimide-Thiol Conjugates." [ACS](https://pubs.acs.org/doi/abs/10.1021/bc5005262)
- Succinimide ring hydrolysis in ADCs (2024). [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10880948/)
- Accelerated stability modeling for bacitracin. [PubMed](https://pubmed.ncbi.nlm.nih.gov/27714699/)
- ICH Q1A(R2) Stability Testing Guideline. [FDA](https://www.fda.gov/media/71707/download)
- Freeze-thaw effects on protein denaturation. [PubMed](https://pubmed.ncbi.nlm.nih.gov/12673768/)
- Freeze-thaw impact on plasma peptides. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC2657648/)
- Strategies for improving peptide stability and delivery (2022). [MDPI](https://www.mdpi.com/1424-8247/15/10/1283)
- BPC-157 multifunctionality review (2025). [MDPI](https://www.mdpi.com/1424-8247/18/2/185)
- Regulatory guidelines for therapeutic peptide analysis (2025). [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11806371/)
- Streamlined LC-MS assay for peptide degradation (2025). [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11507709/)

### Industry and Technical References

- Sigma-Aldrich. "Peptide Stability and Potential Degradation Pathways." [Link](https://www.sigmaaldrich.com/US/en/technical-documents/technical-article/research-and-disease-areas/cell-and-developmental-biology-research/peptide-stability)
- Sigma-Aldrich. "Handling and Storage Guidelines for Peptides and Proteins." [Link](https://www.sigmaaldrich.com/US/en/technical-documents/technical-article/research-and-disease-areas/cell-and-developmental-biology-research/handling-and-storage)
- Bachem. "Handling and Storage Guidelines for Peptides." [Link](https://www.bachem.com/knowledge-center/peptide-guide/handling-and-storage-guidelines-for-peptides/)
- GenScript. "Peptide Storage and Handling Guidelines." [Link](https://www.genscript.com/peptide_storage_and_handling.html)
- JPT Peptide Technologies. "How to Store Peptides." [Link](https://www.jpt.com/blog/store-peptides/)
- AAPPTEC. "Handling and Storage of Peptides." [Link](https://www.peptide.com/faqs/handling-and-storage-of-peptides/)
- Creative Peptides. "Peptide Stability and Shelf Life." [Link](https://www.creative-peptides.com/resources/how-long-do-peptides-last.html)
- ProSpec Bio. Ipamorelin product datasheet. [Link](https://www.prospecbio.com/ipamorelin)
- ProSpec Bio. Bremelanotide product datasheet. [Link](https://www.prospecbio.com/bremelanotide)
- DrugBank. Bremelanotide monograph. [Link](https://go.drugbank.com/drugs/DB11653)
- PubChem. BPC-157 compound data. [Link](https://pubchem.ncbi.nlm.nih.gov/compound/Bpc-157)
- PubChem. Ipamorelin compound data. [Link](https://pubchem.ncbi.nlm.nih.gov/compound/Ipamorelin)

### Vendor and Community Sources

- Vanguard Laboratory. "BPC-157: The Peptide That Won't Sit Still." [Link](https://vanguardlaboratory.com/2026/03/09/bpc-157-the-peptide-that-wont-sit-still-what-testing-actually-reveals/)
- Vanguard Laboratory. "CJC-1295 and Ipamorelin: The Stack Everyone Uses, Nobody Verifies." [Link](https://vanguardlaboratory.com/2026/03/23/cjc-1295-and-ipamorelin-the-stack-everyone-uses-nobody-verifies/)
- Peptpedia. "BPC-157 Stability." [Link](https://peptpedia.org/research/bpc-157-stability)
- Verified Peptides. "Lyophilized Peptide Storage." [Link](https://verifiedpeptides.com/knowledge-hub/lyophilized-peptide-storage-temperature-humidity-light/)
- Peptide Clock. "Visual Inspection Guide: When to Discard Reconstituted Peptides." [Link](https://peptideclock.com/blog/visual-inspection-guide-when-to-discard)
- ACS Lab Testing. "Common Peptide Purity Discrepancies." [Link](https://acslabtest.com/blog/common-peptide-purity-discrepancies-lab-data)
- Container and Packaging. "The Science Behind Amber Glass and UV Protection." [Link](https://www.containerandpackaging.com/resources/The-Science-Behind-Amber-Glass-and-UV-Protection)
- Pacific Vial. "Benefits of Amber, Blue, and Green Glass Vials." [Link](https://pacificvial.com/blogs/news/the-benefits-of-using-amber-blue-and-green-glass-vials-for-light-sensitive-products)
- Biosynth. "Semaglutide Impurities." [Link](https://www.biosynth.com/blog/the-pharmacological-implications-of-semaglutide-impurities)
- BOC Sciences. "Semaglutide and Impurities." [Link](https://www.bocsci.com/products/semaglutide-and-impurities-7249.html)
- Innerbody. "TB4 and TB-500 Peptide Therapy." [Link](https://www.innerbody.com/thymosin-beta-4-and-tb-500)
- Peptide Sciences. "Thymosin Beta-4 vs TB-500." [Link](https://www.peptidesciences.com/peptide-research/thymosin-beta-4-vs-tb-500)
- Spartan Peptides. "PT-141 Bremelanotide Research Guide." [Link](https://spartanpeptides.com/blog/pt-141-bremelanotide-melanocortin-research-guide/)
- Spartan Peptides. "CJC-1295 + Ipamorelin 2026 Research Guide." [Link](https://spartanpeptides.com/blog/cjc-1295-ipamorelin-complete-2026-research-guide/)
- Happy Peptides. "Handling and Stability of Semaglutide." [Link](https://happypeptides.com/blogs/peptide-research/handling-and-stability-of-semaglutide-a-guide-for-laboratory-researchers)

---

*Report generated 2026-03-23. This is an expanded update of RQ-PEP-004_stability.md (2026-03-15). Next scheduled review: Q2 2026.*
