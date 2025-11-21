# Benchmark Analysis Report

*Generated: 2025-11-20 11:52:38*

**Dataset**: 1400 queries across 7 APIs

---

## 1. Performance Rankings

| API | Success Rate | Avg Time | P95 Time | Avg Sources | Avg Answer Length |
|-----|--------------|----------|----------|-------------|-------------------|
| Valyu | 99.8% | 3.48s | 12.07s | 6.3 | 888 |
| You.com | 98.2% | 1.03s | 1.37s | 9.9 | 1030 |
| Exa | 97.9% | 3.02s | 5.72s | 5.8 | 579 |
| Perplexity | 97.4% | 7.90s | 20.46s | 8.9 | 1608 |
| Linkup Standard | 96.8% | 8.09s | 17.75s | 33.7 | 1110 |
| Linkup Deep | 76.0% | 14.73s | 27.66s | 32.6 | 995 |
| Tavily | 43.1% | 2.69s | 7.15s | 8.6 | 188 |

---

## 2. Speed vs Quality Analysis

### Best Value (Characters per Second)

1. **You.com**: 1001.2 chars/sec
   - 1030 characters in 1.03s
   - 9.59 sources per second

2. **Valyu**: 255.2 chars/sec
   - 888 characters in 3.48s
   - 1.81 sources per second

3. **Perplexity**: 203.5 chars/sec
   - 1608 characters in 7.90s
   - 1.12 sources per second

4. **Exa**: 191.8 chars/sec
   - 579 characters in 3.02s
   - 1.92 sources per second

5. **Linkup Standard**: 137.2 chars/sec
   - 1110 characters in 8.09s
   - 4.17 sources per second

6. **Tavily**: 69.7 chars/sec
   - 188 characters in 2.69s
   - 3.21 sources per second

7. **Linkup Deep**: 67.6 chars/sec
   - 995 characters in 14.73s
   - 2.22 sources per second


---

## 3. Reliability Analysis

### Timeout Rates

| API | Total Failures | Timeouts | Timeout Rate |
|-----|----------------|----------|-------------|
| Linkup Deep | 336 | 336 | 24.00% |
| Linkup Standard | 45 | 45 | 3.21% |
| Perplexity | 36 | 35 | 2.50% |
| Valyu | 3 | 3 | 0.21% |
| Exa | 29 | 2 | 0.14% |
| You.com | 25 | 0 | 0.00% |
| Tavily | 796 | 0 | 0.00% |

---

## 4. Competitive Positioning (Linkup)

### Linkup Standard

**Strengths:**
- Significantly more sources than Perplexity (33.7 vs 8.9)
- Significantly more sources than Exa (33.7 vs 5.8)
- Significantly more sources than You.com (33.7 vs 9.9)
- Significantly more sources than Tavily (33.7 vs 8.6)
- Significantly more sources than Valyu (33.7 vs 6.3)

**Areas for Improvement:**
- Lower success rate than Perplexity (96.8% vs 97.4%)
- Lower success rate than Exa (96.8% vs 97.9%)
- Significantly slower than Exa (8.09s vs 3.02s)
- Lower success rate than You.com (96.8% vs 98.2%)
- Significantly slower than You.com (8.09s vs 1.03s)
- Significantly slower than Tavily (8.09s vs 2.69s)
- Lower success rate than Valyu (96.8% vs 99.8%)
- Significantly slower than Valyu (8.09s vs 3.48s)

### Linkup Deep

**Strengths:**
- Significantly more sources than Perplexity (32.6 vs 8.9)
- Significantly more sources than Exa (32.6 vs 5.8)
- Significantly more sources than You.com (32.6 vs 9.9)
- Significantly more sources than Tavily (32.6 vs 8.6)
- Significantly more sources than Valyu (32.6 vs 6.3)

**Critical Issues:**
- ⚠️  CRITICAL: Reduce timeout rate from 336 timeouts (24.0% of queries)

---

## 5. Recommendations

### For Speed-Critical Applications
Use **You.com** - fastest at 1.03s average

### For Maximum Reliability
Use **Valyu** - 99.8% success rate

### For Comprehensive Research
Use **Linkup Standard** - 33.7 sources per query

### CRITICAL: Linkup Deep Optimization
- Reduce timeout rate (currently 336 timeouts)
- Consider implementing progressive timeout strategy
- May need infrastructure scaling
