# Win Rate Methodology Explained

## Overview

The "win rate" measures how often Linkup provides **better value** than a competitor across all 1,400 queries. "Better value" means either **more sources** (when both succeed) or **availability** (when competitor fails).

---

## Win Rate Definition

### Linkup Wins When:
1. **Both APIs succeed** → Linkup has MORE sources (depth advantage)
2. **Only Linkup succeeds** → Competitor times out/fails (availability advantage)

### Competitor Wins When:
1. **Both APIs succeed** → Competitor has MORE sources (depth advantage)
2. **Only Competitor succeeds** → Linkup times out/fails (availability advantage)

### Not Counted:
- **Both fail** → Tie, excluded from calculation
- **Equal sources** → Tie, excluded from calculation (rare: <0.5% of queries)

---

## Example: Linkup vs Perplexity (80.1% Win Rate)

### Breakdown of 1,400 Queries:

| Scenario | Count | % of Total | Winner |
|----------|-------|------------|--------|
| **Both succeed, Linkup has more sources** | 1,082 | 77.3% | 🟢 Linkup |
| **Both succeed, Perplexity has more sources** | 234 | 16.7% | 🔴 Perplexity |
| **Both succeed, equal sources** | 5 | 0.4% | - (not counted) |
| **Only Linkup succeeds** | 34 | 2.4% | 🟢 Linkup |
| **Only Perplexity succeeds** | 43 | 3.1% | 🔴 Perplexity |
| **Both fail** | 2 | 0.1% | - (not counted) |

### Win Calculation:
```
Linkup Wins = 1,082 (more sources) + 34 (availability) = 1,116
Perplexity Wins = 234 (more sources) + 43 (availability) = 277
Total Comparable = 1,116 + 277 = 1,393

Win Rate = 1,116 / 1,393 = 80.1%
```

### Key Insight:
- **Primary advantage**: Source depth (77.3% of queries have more sources)
- **Average source advantage**: +31.6 sources when Linkup wins
- **Secondary factor**: Availability (2.4% vs 3.1% - slightly behind)

---

## All Competitors Breakdown

### Linkup vs Tavily (97.3% Win Rate)

| Metric | Count | Details |
|--------|-------|---------|
| **Linkup wins** | 1,315 | 559 (more sources) + 756 (availability) |
| **Tavily wins** | 36 | 31 (more sources) + 5 (availability) |
| **Win rate** | 97.3% | Complete dominance |

**Analysis**: Tavily has poor reliability (43.1% success rate), so Linkup wins primarily on **availability** (756 queries where Tavily failed).

---

### Linkup vs Valyu (88.9% Win Rate)

| Metric | Count | Details |
|--------|-------|---------|
| **Linkup wins** | 1,220 | 755 (more sources) + 465 (availability) |
| **Valyu wins** | 153 | 135 (more sources) + 18 (availability) |
| **Win rate** | 88.9% | Strong advantage |

**Analysis**: Valyu has low success rate (64.9% with "No results found" excluded), so Linkup wins heavily on **availability** (465 queries where Valyu couldn't answer).

---

### Linkup vs Exa (86.5% Win Rate)

| Metric | Count | Details |
|--------|-------|---------|
| **Linkup wins** | 1,125 | 1,098 (more sources) + 27 (availability) |
| **Exa wins** | 175 | 132 (more sources) + 43 (availability) |
| **Win rate** | 86.5% | Strong advantage |

**Analysis**: Exa has high reliability (97.9%), so Linkup wins primarily on **source depth** (1,098 queries with more sources). Average advantage: 5.8x more sources (33.7 vs 5.8).

---

### Linkup vs Perplexity (80.1% Win Rate)

| Metric | Count | Details |
|--------|-------|---------|
| **Linkup wins** | 1,116 | 1,082 (more sources) + 34 (availability) |
| **Perplexity wins** | 277 | 234 (more sources) + 43 (availability) |
| **Win rate** | 80.1% | Solid advantage |

**Analysis**: Perplexity has high reliability (97.4%) and decent sources (8.9), so competition is tighter. Linkup still wins 77% on **source depth**. Average advantage: 3.8x more sources (33.7 vs 8.9).

---

### Linkup vs You.com (79.6% Win Rate)

| Metric | Count | Details |
|--------|-------|---------|
| **Linkup wins** | 1,113 | 1,089 (more sources) + 24 (availability) |
| **You.com wins** | 286 | 242 (more sources) + 44 (availability) |
| **Win rate** | 79.6% | Solid advantage |

**Analysis**: You.com has highest reliability (98.2%) and decent sources (9.9), making this the **closest competition**. Linkup wins 77.8% on **source depth**. Average advantage: 3.4x more sources (33.7 vs 9.9).

**Note**: You.com is **7.9x faster** (1.03s vs 8.09s), so they win on speed despite losing on depth.

---

## What Win Rate Means for Different Use Cases

### High Win Rate = Strong Position

| Win Rate | Interpretation | Action |
|----------|----------------|--------|
| **90%+** | Dominant (Tavily, Valyu) | Direct substitution, competitive messaging |
| **80-90%** | Strong advantage (Exa) | Head-to-head comparisons work well |
| **75-80%** | Solid advantage (Perplexity, You.com) | Emphasize specific strengths (depth vs speed) |
| **<75%** | Competitive market | Differentiate on use case, not direct comparison |

### Win Rate Composition Matters

**Example 1: Tavily (97.3%)**
- 756 wins from availability
- 559 wins from source depth
- **Interpretation**: Linkup wins because Tavily is unreliable, not because Linkup is dramatically better

**Example 2: Exa (86.5%)**
- 1,098 wins from source depth
- 27 wins from availability
- **Interpretation**: Linkup wins on **quality** (more sources), not just availability
- **This is a stronger competitive position**

---

## Strategic Implications

### 1. Source Depth is Linkup's Moat

In matchups with reliable competitors (Exa, Perplexity, You.com):
- 77-83% of wins come from **source depth**
- Only 2-3% of wins come from availability
- **Takeaway**: Depth advantage is real and consistent

### 2. Speed vs Depth Trade-off

**You.com comparison reveals the market tension:**
- Linkup: 79.6% win rate (depth)
- You.com: 7.9x faster (speed)

**Market segments:**
- **Depth-sensitive** → Linkup wins (research, B2B, due diligence)
- **Speed-sensitive** → You.com wins (chatbots, real-time, customer-facing)

### 3. Reliability Unlocks Value

**Against unreliable competitors** (Tavily, Valyu):
- Win rate boosted by availability advantage
- But less meaningful for competitive positioning
- These aren't Linkup's real competitors

**Against reliable competitors** (Exa, Perplexity, You.com):
- Win rate depends on source depth
- These ARE Linkup's real competitors
- 80% win rate proves depth advantage

---

## Limitations of Win Rate Metric

### What It Doesn't Capture:

1. **Answer Quality**
   - More sources ≠ better answer
   - Need LLM evaluation for quality

2. **Speed**
   - You.com is 7.9x faster
   - Win rate ignores latency trade-offs

3. **User Experience**
   - Source presentation matters
   - API ergonomics not measured

4. **Cost**
   - No pricing consideration
   - ROI not factored in

5. **Use Case Fit**
   - 33 sources might be overkill for simple queries
   - 10 sources might be insufficient for research

### What It Does Capture:

✅ **Comprehensive coverage** (source depth)
✅ **Reliability** (availability advantage)
✅ **Consistency** across 1,400 diverse queries
✅ **Competitive positioning** for depth-focused use cases

---

## Recommended Usage

### For Marketing:
- **Use win rate** when emphasizing comprehensive coverage
- **Don't use win rate** when competing on speed or simplicity

### For Sales:
- **80%+ win rate** → Strong competitive talking point
- Explain it's about **depth**, not speed
- Target customers who value comprehensive data

### For Product:
- **High win rate** validates source aggregation strategy
- **20% losses** show where competitors have advantages
- Analyze losses to find improvement opportunities

### For Strategy:
- **79-86% against top competitors** → Linkup has a defensible moat
- **Depth wins consistently** → Double down on this advantage
- **Speed losses** → Either fix speed OR target depth-sensitive segments

---

## Conclusion

**Linkup's 79-97% win rates mean:**

1. **Linkup provides more sources** in 75-83% of queries (vs reliable competitors)
2. **Linkup is more reliable** than Tavily/Valyu (but not vs Exa/Perplexity/You.com)
3. **Depth advantage is consistent** across diverse query types
4. **This is a defensible moat** - no competitor is close to 33.7 avg sources

**But remember:**
- Win rate optimizes for **depth**, not **speed**
- You.com is faster but Linkup still wins 79.6% on depth
- Different customers optimize for different metrics
- Target customers who value **comprehensive coverage** over **speed**

