# Benchmark Analysis Report (Corrected)

*Generated: 2025-11-21 03:10:00*

**Dataset**: 1400 queries across 7 APIs

**Note**: Valyu analysis corrected to exclude "No results found" responses from success rate calculations.

---

## 1. Performance Rankings

| API | Success Rate | Avg Time | P95 Time | Avg Sources | Avg Answer Length | Chars/Sec |
|-----|--------------|----------|----------|-------------|-------------------|-----------|
| You.com | 98.2% | 1.03s | 1.37s | 9.9 | 1030 | 1001.2 |
| Exa | 97.9% | 3.02s | 5.72s | 5.8 | 579 | 191.8 |
| Perplexity | 97.4% | 7.90s | 20.46s | 8.9 | 1608 | 203.5 |
| Linkup Standard | 96.8% | 8.09s | 17.75s | 33.7 | 1112 | 137.5 |
| Linkup Deep | 76.0% | 14.73s | 27.66s | 32.6 | 995 | 67.6 |
| **Valyu** | **64.9%** | 4.10s | 11.30s | 9.7 | 1373 | 334.7 |
| Tavily | 43.1% | 2.69s | 7.15s | 8.6 | 188 | 69.9 |

### Key Changes from Previous Analysis

**Valyu Performance Update:**
- **Previous (incorrect)**: 99.8% success rate
- **Corrected**: 64.9% success rate (908/1400 queries)
- **Reason**: Original analysis counted "No results found" (492 queries, 35.1%) as successful responses
- **Technical Success**: 100% (API always responds)
- **Actual Answers**: 908 queries with real data

---

## 2. Speed vs Quality Analysis

### Best Value (Characters per Second)

1. **You.com**: 1001.2 chars/sec ⭐
   - 1030 characters in 1.03s
   - 9.9 sources
   - 98.2% success rate

2. **Valyu**: 334.7 chars/sec
   - 1373 characters in 4.10s
   - 9.7 sources
   - ⚠️  Only 64.9% success rate (many queries unsupported)

3. **Perplexity**: 203.5 chars/sec
   - 1608 characters in 7.90s
   - 8.9 sources
   - 97.4% success rate

4. **Exa**: 191.8 chars/sec
   - 579 characters in 3.02s
   - 5.8 sources
   - 97.9% success rate

5. **Linkup Standard**: 137.5 chars/sec
   - 1112 characters in 8.09s
   - 33.7 sources ⭐ (highest)
   - 96.8% success rate

6. **Tavily**: 69.9 chars/sec
   - 188 characters in 2.69s
   - 8.6 sources
   - ⚠️  Only 43.1% success rate

7. **Linkup Deep**: 67.6 chars/sec
   - 995 characters in 14.73s
   - 32.6 sources
   - ⚠️  Only 76.0% success rate (24% timeout rate)

---

## 3. Valyu Detailed Analysis

### What Valyu Cannot Handle (35.1% of queries)

The 492 "No results found" responses fall into these categories:

1. **Website Summarization Requests** (~250 queries)
   - Example: *"Visit the website https://example.com and provide a comprehensive description..."*
   - Valyu cannot scrape and summarize arbitrary websites

2. **Company Research with Specific URLs** (~150 queries)
   - Example: *"I'm researching the company XYZ. Please use their website (http://xyz.com) as the primary source..."*
   - Requires direct website content extraction

3. **French Company Analysis** (~85 queries)
   - Example: *"Analyse l'entreprise ci-dessous en menant une recherche approfondie..."*
   - Complex analysis requiring specific company data

4. **Insurance Broker Capability Queries** (~7 queries)
   - Example: *"We are trying to evaluate whether the company offers Cyber insurance..."*
   - Niche domain-specific queries

### What Valyu Handles Well (64.9% of queries)

1. **General Knowledge Queries**
2. **Technical Documentation Searches**
3. **Recent News and Events**
4. **CVE Vulnerability Research**
5. **LinkedIn Profile Research**
6. **Competitive Analysis**

### Valyu Performance (For Supported Queries)

- **Response Time**: 4.10s average (competitive)
- **Answer Quality**: 1373 chars average (second highest)
- **Sources**: 9.7 per query (good)
- **Chars/Sec**: 334.7 (second fastest among successful queries)

---

## 4. Reliability Analysis

### Timeout Rates

| API | Total Failures | Timeouts | Timeout Rate | Failure Type |
|-----|----------------|----------|-------------|--------------|
| Linkup Deep | 336 | 336 | 24.00% | ⚠️  Timeout |
| Linkup Standard | 45 | 45 | 3.21% | Timeout |
| Perplexity | 36 | 35 | 2.50% | Timeout |
| **Valyu** | **492** | **0** | **0.00%** | ⚠️  **Unsupported Query Type** |
| Exa | 29 | 2 | 0.14% | Mixed |
| You.com | 25 | 0 | 0.00% | Mixed |
| Tavily | 796 | 0 | 0.00% | Mixed |

**Key Insight**: Valyu's 35.1% "failure" rate is fundamentally different from other APIs:
- **Not a technical failure**: API responds reliably
- **Capability limitation**: Cannot handle website scraping/summarization queries
- **No timeouts**: Always responds quickly, even when unable to fulfill request

---

## 5. Competitive Positioning (Linkup)

### Linkup Standard

**Strengths:**
- ⭐ **Significantly more sources** than all competitors (33.7 vs 5.8-9.9)
  - 3.8x more than Exa
  - 3.4x more than Valyu
  - 3.8x more than Perplexity
- Strong answer quality (1112 chars)
- High success rate (96.8%)

**Areas for Improvement:**
- **Speed**: 8.09s average (slower than You.com, Exa, Valyu, Tavily)
  - 7.9x slower than You.com (1.03s)
  - 2.7x slower than Exa (3.02s)
  - 2.0x slower than Valyu (4.10s)
- **Success Rate**: Slightly lower than top 3 competitors
  - 1.4% behind You.com (98.2%)
  - 1.1% behind Exa (97.9%)
  - 0.6% behind Perplexity (97.4%)
- **Timeout Rate**: 3.21% (45 queries)

**Unique Value Proposition:**
- Best for comprehensive research requiring maximum source coverage
- Significantly outperforms on source richness (3-4x more sources)

### Linkup Deep

**Strengths:**
- ⭐ **Second-highest source count** (32.6 sources)
- Comprehensive answers (995 chars)

**Critical Issues:**
- ⚠️  **CRITICAL: 24.0% timeout rate** (336 queries)
  - Highest timeout rate among all APIs
  - 7.5x higher than Linkup Standard (3.21%)
- **Slow**: 14.73s average
  - 14.3x slower than You.com
  - 4.9x slower than Exa
  - 1.8x slower than Linkup Standard
- **Low Success Rate**: 76.0% (only beats Tavily)

**Recommendation**:
- Urgent optimization needed for timeout handling
- Consider progressive timeout strategy
- May need infrastructure scaling or query complexity analysis

---

## 6. Updated Recommendations

### For Speed-Critical Applications
**Use You.com** ⭐
- Fastest at 1.03s average
- 98.2% success rate
- 1001.2 chars/sec throughput
- Good source coverage (9.9 sources)

### For Maximum Reliability (General Queries)
**Use You.com or Exa**
- You.com: 98.2% success rate
- Exa: 97.9% success rate
- Both have near-zero timeout rates

### For Comprehensive Research
**Use Linkup Standard** ⭐
- 33.7 sources per query (3-4x more than competitors)
- 96.8% success rate (competitive)
- Best for in-depth analysis requiring multiple sources

### For Balanced Performance
**Use Perplexity**
- 97.4% success rate
- Best answer length (1608 chars)
- Good source coverage (8.9 sources)
- Acceptable speed (7.90s)

### When to Avoid Valyu
❌ **Do NOT use Valyu for**:
- Website summarization requests
- Company research requiring specific website content
- Any query starting with "Visit the website..."
- Queries requiring direct URL content extraction

✅ **Use Valyu for**:
- General knowledge queries
- Recent news/events
- Technical documentation
- CVE research
- LinkedIn analysis
- Fast-paced chars/sec when query is supported (334.7 chars/sec)

---

## 7. Critical Action Items

### Priority 1: Linkup Deep Timeout Optimization
- **Current State**: 24% timeout rate (336/1400 queries)
- **Impact**: Severely limits usability
- **Actions**:
  1. Analyze query patterns causing timeouts
  2. Implement progressive timeout strategy
  3. Consider query complexity pre-screening
  4. Infrastructure scaling assessment

### Priority 2: Linkup Standard Speed Optimization
- **Current State**: 8.09s average (2-8x slower than top competitors)
- **Impact**: Limits adoption for speed-sensitive use cases
- **Actions**:
  1. Optimize parallel source fetching
  2. Implement smart caching
  3. Consider reducing source count for speed-critical mode
  4. Benchmark infrastructure bottlenecks

### Priority 3: Valyu Query Routing
- **Current State**: 35.1% queries unsupported by design
- **Impact**: Misleading success metrics if not handled properly
- **Actions**:
  1. Pre-screen queries before sending to Valyu
  2. Implement query type classification
  3. Route website scraping queries to alternative APIs
  4. Update documentation on Valyu limitations

---

## 8. Market Positioning Summary

### Top Tier (>95% Success Rate)
1. **You.com** (98.2%) - Speed leader
2. **Exa** (97.9%) - Balanced performer
3. **Perplexity** (97.4%) - Quality leader
4. **Linkup Standard** (96.8%) - Research depth leader ⭐

### Mid Tier (65-80% Success Rate)
5. **Linkup Deep** (76.0%) - ⚠️  Needs timeout fixes
6. **Valyu** (64.9%) - ⚠️  Limited query support

### Low Tier (<50% Success Rate)
7. **Tavily** (43.1%) - Significant reliability issues

**Linkup's Competitive Edge**:
- **Source richness** (3-4x more sources than competitors)
- Strong reliability (96.8% for Standard)
- Opportunity to improve speed while maintaining depth advantage

