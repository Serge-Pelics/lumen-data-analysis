# Methodology

Version 0.1. This document describes how the project measures what it claims to
measure. It is written before large-scale data collection so that thresholds and
decision rules are fixed in advance rather than chosen after seeing which ones
produce interesting results.

## 1. Purpose and scope

The project studies whether **template-driven and likely abusive copyright
removal requests can be identified in public transparency data**, using notice
metadata rather than case-by-case legal review.

The output is a written report with aggregate findings, published together with
the analysis code so that the numbers can be reproduced and disputed.

## 2. Research questions

- **RQ1.** To what extent is notice language reused across unrelated recipients,
  and can that reuse be measured stably under different text-normalisation
  choices?
- **RQ2.** Do notices arrive in temporal bursts, and does burst structure differ
  when many distinct sender identities participate in the same burst?
- **RQ3.** How often does a notice name an "original work" location whose
  earliest observable existence postdates the page it accuses?
- **RQ4.** Which categories of target pages are disproportionately represented,
  and does that distribution differ between clustered and unclustered notices?

## 3. What this study does not claim

These boundaries are part of the method, not a disclaimer bolted on afterwards.

- It does **not** determine whether any individual notice is lawful. Validity
  under the DMCA depends on facts not present in the archive, including who owns
  the work and whether a use is fair.
- It does **not** treat template reuse as evidence of abuse on its own. Large
  legitimate rights-enforcement operations use templates heavily; boilerplate is
  the norm in this corpus, not the anomaly. Template reuse is only informative in
  conjunction with other signals (§7).
- It does **not** name or profile individual senders in published output.
- It does **not** describe the population of all removal requests. It describes
  the population of requests **present in Lumen**, which is different (§10).

## 4. Data

**Source.** The Lumen Database API, accessed with researcher credentials under
its Terms of Use. Requests carry a descriptive User-Agent and respect the rate
limit agreed with Lumen staff.

**Fields used.** Notice identifier, notice type, date received, sender and
principal, recipient, jurisdiction, topics and tags, action taken, and for each
work the counts and hostnames of the claimed original and claimed infringing
locations. Notice body text is used for §6.1 where it is available.

**Redaction.** Parts of the archive are redacted for privacy. Redaction is
treated as a data property, not noise: for every reported figure the denominator
is the number of notices where the relevant field was actually present, and that
denominator is stated alongside the figure. Records missing a field are never
silently counted as negative cases.

**Storage.** Retrieved records are cached locally so that analysis reruns do not
re-query the API. The cache is not redistributed (§11).

## 5. Unit of analysis

Three levels, kept explicitly separate because conflating them is the easiest way
to produce inflated numbers:

| Level | Unit | Used for |
|---|---|---|
| Notice | one submitted notice | burst detection, template clustering |
| Work | one claimed work inside a notice | provenance checks |
| URL | one listed location | target categorisation, counts |

A single notice may list thousands of URLs. Reporting "URLs affected" and
"notices sent" as if they were comparable magnitudes is a known failure mode in
this literature, so every count states its unit.

## 6. Signal operationalisation

### 6.1 S1: template reuse

**Normalisation.** Before comparison, notice text is lowercased and the
following are replaced with typed placeholders: URLs, bare hostnames, email
addresses, dates, monetary amounts, standalone numbers, and any occurrence of the
sender, principal, or recipient name. The purpose is to leave the *frame* of the
notice and remove the specifics, so that two notices about entirely different
works can still be recognised as the same document.

**Comparison.** Normalised text is shingled into overlapping word 5-grams.
Pairwise Jaccard similarity is estimated with MinHash signatures (128 permutations)
and candidate pairs are retrieved with locality-sensitive hashing, which keeps the
comparison tractable without evaluating all pairs.

**Clustering.** Pairs at or above a similarity threshold form an undirected
graph; clusters are its connected components. The primary threshold is
**J ≥ 0.80**, fixed in advance. Because connected-component clustering can chain
dissimilar documents together through intermediates, every cluster reports its
internal density, and clusters whose density falls below 0.5 are flagged and
inspected rather than reported as single templates.

**Sensitivity.** All cluster-level results are recomputed at J ∈ {0.70, 0.75,
0.85, 0.90} and with 3-gram and 7-gram shingles. A finding that only survives at
one parameter setting is reported as unstable, not as a finding.

**Cluster descriptors.** Size in notices, number of distinct senders, number of
distinct recipients, number of distinct target hostnames, and time span.

### 6.2 S2: temporal bursts

Daily notice counts are computed per sender and per target hostname. A negative
binomial baseline is fitted on a trailing 90-day window to accommodate the
overdispersion typical of this data; a day is a candidate burst when its count
exceeds the 99th percentile of the fitted baseline. Consecutive candidate days
merge into one burst.

Reported per burst: peak count, duration, ratio of peak to trailing median, and
the number of distinct sender identities active during it. The last descriptor
carries most of the analytical weight, because a burst from one established
sender is ordinary operational behaviour, while a synchronised burst across many
newly appearing sender identities is not.

Bursts overlapping known external events, such as a film release, are annotated
so that they are not read as coordination.

### 6.3 S3: provenance implausibility

For a work naming both a claimed original location and a claimed infringing
location, two observable dates are collected:

- earliest capture of each URL in the Internet Archive, via the CDX API;
- registration date of each hostname, via RDAP where published.

A work is flagged when the claimed original location has **no observable
existence before** the claimed infringing location, by both measures, with a
30-day margin to absorb crawl-timing error.

**Interpretation limits, stated up front.** Absence from the Internet Archive is
not absence from the web; crawl coverage is uneven and skews toward popular
sites. Domain registration predates publication by an unknown interval. Neither
measure establishes authorship. Consequently S3 is reported as *unverifiable
provenance*, never as *false claim*, and its rate is always accompanied by the
share of works where neither date could be obtained at all.

### 6.4 S4: target page type

Target URLs are coded into: media file or stream, storefront or download page,
editorial or review page, forum or user-generated page, search or index page,
and other. A stratified random sample is coded by hand against a written codebook
with worked examples; the codebook is published with the report. A classifier is
trained only if hand-coding agreement is acceptable (§8.3), and its output is
used for description, never as the sole basis for a headline claim.

## 7. Combining signals

No single signal is treated as an abuse indicator. The analysis reports the
**joint distribution** of S1 to S4 and examines whether conjunctions are more
concentrated than independence would predict.

The conjunction of primary interest is a template cluster that spans many
distinct sender identities, appears in a synchronised burst, and shows
unverifiable provenance. That combination is hard to produce as a by-product of
ordinary enforcement, which is precisely why it is worth measuring. It is
reported as an elevated-concern pattern with a rate and an interval, not as a
determination about any notice or sender.

## 8. Validation

The central methodological problem is that **no ground truth for "false notice"
exists in the archive**. The study addresses this rather than assuming it away.

### 8.1 Reference sets

Two small positive reference sets are assembled from outside the archive:
notices that drew a counter-notification recorded in Lumen, and notices publicly
retracted or found abusive in reporting or court records. A negative reference
set is drawn from notices sent by long-established rights holders about
first-party media. Both sets are small and non-representative; they are used to
check that the signals behave in the expected direction, not to estimate
population rates.

### 8.2 Manual adjudication

Precision is estimated on stratified random samples of flagged and unflagged
cases, adjudicated by hand against the codebook and reported with Wilson score
intervals. Sample sizes are set in advance for a target interval half-width of
10 percentage points.

### 8.3 Reliability

As a solo researcher I cannot compute conventional inter-coder agreement. In its
place, a 15 percent subsample is re-coded blind after at least 14 days, and
test-retest agreement is reported as Cohen's kappa. Agreement below 0.7 sends the
codebook back for revision before any coded result is published.

### 8.4 Pre-registration

Thresholds in §6, sample sizes in §8.2, and the conjunction in §7 are fixed in
this document before full collection. Any later change is recorded in §13 with
its date and reason, so that readers can see what was decided before the data
and what after.

## 9. Reporting

Counts always state their unit and denominator. Proportions carry confidence
intervals. Time series state the aggregation window. Where a figure depends on a
threshold, the sensitivity range accompanies it. Null and inconclusive results
are reported, including signals that turn out not to discriminate.

## 10. Limitations

- **Coverage.** Lumen contains notices that recipients chose to submit. Senders,
  platforms, and jurisdictions are unevenly represented, and the archive is not a
  sample of all removal requests. No population estimate is offered.
- **Redaction** removes fields unevenly, which can correlate with notice type.
- **Body text availability** limits S1 to the subset where text is present.
- **Archive and registration data** are proxies with the weaknesses in §6.3.
- **Template detection** is sensitive to normalisation; §6.1 reports the range
  rather than a single number.
- **No legal conclusion** follows from any measurement here.

## 11. Ethics and data handling

- Personal contact details are not republished. Findings are aggregate.
- Individual senders, principals, and recipients are not named in published
  output except where already the subject of public reporting or court record.
- Complainants are not contacted, pressured, or otherwise approached as a result
  of this analysis.
- Raw retrieved records are not redistributed. Published artefacts are derived
  aggregates plus code, so that another researcher with their own credentials can
  reproduce the result without the archive being mirrored.
- Lumen is credited as the source in all published output, and the rate limits
  and Terms of Use governing access are followed.

## 12. Reproducibility

- Analysis code is released under the MIT licence in this repository.
- Dependencies are version-pinned; the interpreter version is recorded.
- Thresholds live in a configuration file, not scattered through the code, so a
  reviewer can re-run the study under different assumptions in one place.
- Random seeds are fixed and recorded for sampling and for MinHash permutations.
- Each published figure names the script and configuration that produced it.

## 13. Change log

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-07-29 | First version, written before large-scale collection. |
