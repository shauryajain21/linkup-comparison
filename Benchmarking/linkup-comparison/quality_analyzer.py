#!/usr/bin/env python3
"""
Advanced quality analysis for API responses
Identifies competitive advantages and use cases
"""

import json
import csv
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any
import re
from collections import Counter

class APIResponseAnalyzer:
    def __init__(self):
        self.quality_metrics = []

    def analyze_response_quality(self, query: str, responses: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze quality metrics for each API's response to a query
        """
        metrics = {"query": query}

        for api_name, response_data in responses.items():
            answer = response_data.get("answer", "")
            sources = response_data.get("sources", [])
            response_time = response_data.get("response_time", 0)

            # Calculate quality metrics
            metrics[f"{api_name}_metrics"] = {
                "completeness_score": self.score_completeness(answer, query),
                "specificity_score": self.score_specificity(answer),
                "source_quality": self.score_source_quality(sources),
                "response_time": response_time,
                "word_count": len(answer.split()),
                "has_numbers": bool(re.search(r'\d+', answer)),
                "has_specific_names": self.has_specific_names(answer),
                "confidence_level": self.score_confidence(answer),
                "actionability": self.score_actionability(answer)
            }

        # Determine winner for this query
        metrics["winner"] = self.determine_winner(metrics)
        metrics["win_reason"] = self.explain_win(metrics)

        return metrics

    def score_completeness(self, answer: str, query: str) -> float:
        """Score how completely the answer addresses the query"""
        score = 0.0

        # Check if answer directly addresses the question
        query_keywords = set(query.lower().split())
        answer_lower = answer.lower()

        # Remove common words
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        query_keywords = query_keywords - stop_words

        # Check keyword coverage
        keywords_found = sum(1 for kw in query_keywords if kw in answer_lower)
        if query_keywords:
            score = keywords_found / len(query_keywords)

        # Bonus for specific numbers/data
        if re.search(r'\d+', answer):
            score += 0.2

        # Bonus for direct answer format
        if answer.strip() and not answer.lower().startswith(("i don't", "i cannot", "the exact")):
            score += 0.1

        return min(score, 1.0)

    def score_specificity(self, answer: str) -> float:
        """Score how specific vs vague the answer is"""
        score = 0.5  # Start neutral

        # Specific indicators (good)
        specific_patterns = [
            r'\d+',  # Numbers
            r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',  # Dates
            r'\$[\d,]+',  # Money
            r'\d+%',  # Percentages
            r'[A-Z][a-z]+ [A-Z][a-z]+',  # Proper names
        ]

        for pattern in specific_patterns:
            if re.search(pattern, answer):
                score += 0.1

        # Vague indicators (bad)
        vague_phrases = [
            'multiple', 'various', 'several', 'many', 'some',
            'exact number is not specified', 'approximately',
            'it depends', 'varies', 'unclear'
        ]

        answer_lower = answer.lower()
        for phrase in vague_phrases:
            if phrase in answer_lower:
                score -= 0.15

        return max(0, min(score, 1.0))

    def score_source_quality(self, sources: List[Dict]) -> float:
        """Score the quality and relevance of sources"""
        if not sources:
            return 0.0

        score = min(len(sources) * 0.2, 0.6)  # Base score for having sources

        # Check for authoritative domains
        authoritative_domains = ['.gov', '.edu', '.org', 'official', 'optum.com']
        for source in sources:
            url = source.get('url', '') if isinstance(source, dict) else str(source)
            for domain in authoritative_domains:
                if domain in url.lower():
                    score += 0.1
                    break

        return min(score, 1.0)

    def score_confidence(self, answer: str) -> float:
        """Score the confidence level of the answer"""
        score = 0.7  # Start with moderate confidence

        # High confidence indicators
        confident_phrases = ['specifically', 'exactly', 'definitely', 'clearly', 'total of']

        # Low confidence indicators
        uncertain_phrases = [
            'may', 'might', 'possibly', 'appears', 'seems',
            'not specified', 'unclear', 'approximately', 'about'
        ]

        answer_lower = answer.lower()

        for phrase in confident_phrases:
            if phrase in answer_lower:
                score += 0.15

        for phrase in uncertain_phrases:
            if phrase in answer_lower:
                score -= 0.1

        return max(0, min(score, 1.0))

    def score_actionability(self, answer: str) -> float:
        """Score how actionable the answer is"""
        score = 0.5

        # Actionable indicators
        action_patterns = [
            r'call \d{3}-\d{3}-\d{4}',  # Phone numbers
            r'visit [a-zA-Z]+\.com',  # Website references
            r'contact',
            r'schedule',
            r'locate'
        ]

        for pattern in action_patterns:
            if re.search(pattern, answer, re.IGNORECASE):
                score += 0.2

        # Direct answer is actionable
        if re.search(r'\d+ (locations?|offices?|centers?)', answer):
            score += 0.3

        return min(score, 1.0)

    def has_specific_names(self, answer: str) -> bool:
        """Check if answer contains specific location/entity names"""
        # Look for capitalized words (proper nouns)
        proper_nouns = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', answer)
        return len(proper_nouns) > 2

    def determine_winner(self, metrics: Dict) -> str:
        """Determine which API gave the best response"""
        api_scores = {}

        for key in metrics:
            if key.endswith("_metrics"):
                api_name = key.replace("_metrics", "")
                api_metrics = metrics[key]

                # Calculate weighted score
                score = (
                    api_metrics["completeness_score"] * 0.3 +
                    api_metrics["specificity_score"] * 0.25 +
                    api_metrics["source_quality"] * 0.15 +
                    api_metrics["confidence_level"] * 0.15 +
                    api_metrics["actionability"] * 0.15
                )

                # Penalty for slow response
                if api_metrics["response_time"] > 1.0:
                    score *= 0.9

                api_scores[api_name] = score

        if not api_scores:
            return "none"

        return max(api_scores, key=api_scores.get)

    def explain_win(self, metrics: Dict) -> str:
        """Explain why the winner was chosen"""
        winner = metrics.get("winner", "none")
        if winner == "none":
            return "No clear winner"

        winner_metrics = metrics.get(f"{winner}_metrics", {})
        reasons = []

        if winner_metrics.get("has_numbers"):
            reasons.append("provides specific numbers")
        if winner_metrics.get("specificity_score", 0) > 0.7:
            reasons.append("gives specific details")
        if winner_metrics.get("source_quality", 0) > 0.5:
            reasons.append("has quality sources")
        if winner_metrics.get("confidence_level", 0) > 0.7:
            reasons.append("confident answer")
        if winner_metrics.get("response_time", 999) < 0.5:
            reasons.append("fast response")

        return "; ".join(reasons) if reasons else "overall better quality"


def identify_use_cases(analysis_results: List[Dict]) -> Dict[str, List[str]]:
    """
    Identify specific use cases where each API excels
    """
    use_cases = {
        "quantitative_queries": [],  # Queries asking for numbers
        "location_queries": [],      # Queries about places
        "comparison_queries": [],    # Queries comparing things
        "factual_queries": [],       # Simple fact lookups
        "complex_queries": []        # Multi-part questions
    }

    for result in analysis_results:
        query = result["query"]
        winner = result.get("winner", "")

        # Classify query type
        query_lower = query.lower()

        if any(word in query_lower for word in ["how many", "count", "number", "total", "percentage"]):
            use_cases["quantitative_queries"].append(f"{query} -> Winner: {winner}")

        if any(word in query_lower for word in ["where", "location", "place", "address", "california"]):
            use_cases["location_queries"].append(f"{query} -> Winner: {winner}")

        if any(word in query_lower for word in ["compare", "versus", "vs", "difference", "better"]):
            use_cases["comparison_queries"].append(f"{query} -> Winner: {winner}")

        if "?" in query and len(query.split()) < 10:
            use_cases["factual_queries"].append(f"{query} -> Winner: {winner}")

        if len(query.split()) > 15 or query.count(",") > 2:
            use_cases["complex_queries"].append(f"{query} -> Winner: {winner}")

    return use_cases


def generate_quality_report(input_file: str, output_dir: str = "."):
    """
    Generate comprehensive quality analysis report
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    # Load data
    with open(input_file, 'r') as f:
        data = json.load(f)

    analyzer = APIResponseAnalyzer()
    analysis_results = []

    # Analyze each query
    for item in data:
        query = item.get("query", "")

        # Organize responses by API
        responses_by_api = {}
        for response in item.get("responses", []):
            api_name = response.get("api_name", "")
            response_data_raw = response.get("response_data", {})

            # Handle None response_data
            if response_data_raw is None:
                response_data_raw = {}

            # Extract answer and sources based on API format
            answer = response_data_raw.get("answer", "") or response_data_raw.get("content", "")
            sources = response_data_raw.get("sources", [])

            responses_by_api[api_name] = {
                "answer": answer,
                "sources": sources,
                "response_time": response.get("response_time", 0)
            }

        # Analyze quality
        metrics = analyzer.analyze_response_quality(query, responses_by_api)
        analysis_results.append(metrics)

    # Generate reports
    # 1. Quality metrics CSV
    quality_df = pd.DataFrame(analysis_results)
    quality_df.to_csv(output_dir / "quality_analysis.csv", index=False)

    # 2. Win rate summary
    win_counts = Counter(r["winner"] for r in analysis_results)
    win_rate_df = pd.DataFrame(
        [(api, count, count/len(analysis_results)*100)
         for api, count in win_counts.items()],
        columns=["API", "Wins", "Win_Rate_%"]
    )
    win_rate_df.to_csv(output_dir / "win_rates.csv", index=False)

    # 3. Use cases identification
    use_cases = identify_use_cases(analysis_results)

    with open(output_dir / "use_cases.txt", 'w') as f:
        f.write("=== USE CASE ANALYSIS ===\n\n")
        for use_case, queries in use_cases.items():
            f.write(f"\n{use_case.upper()}:\n")
            f.write("-" * 40 + "\n")
            for q in queries[:10]:  # Top 10 examples
                f.write(f"  • {q}\n")

    # 4. Competitive advantages summary
    advantages = []
    for result in analysis_results:
        if result.get("winner"):
            advantages.append({
                "query": result["query"],
                "winner": result["winner"],
                "reason": result["win_reason"]
            })

    advantages_df = pd.DataFrame(advantages)
    advantages_df.to_csv(output_dir / "competitive_advantages.csv", index=False)

    # Print summary
    print("=== QUALITY ANALYSIS REPORT ===")
    print(f"\nTotal queries analyzed: {len(analysis_results)}")
    print("\nWin rates by API:")
    for api, count in win_counts.items():
        print(f"  {api}: {count} wins ({count/len(analysis_results)*100:.1f}%)")

    print("\nReports generated:")
    print(f"  • quality_analysis.csv - Detailed metrics for each query")
    print(f"  • win_rates.csv - Summary of win rates")
    print(f"  • use_cases.txt - Identified use cases")
    print(f"  • competitive_advantages.csv - Where each API excels")

    return analysis_results


# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else "quality_analysis"
        generate_quality_report(input_file, output_dir)
    else:
        print("Usage: python quality_analyzer.py <input_json> [output_dir]")
