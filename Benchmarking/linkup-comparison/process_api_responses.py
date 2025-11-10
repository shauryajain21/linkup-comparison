#!/usr/bin/env python3
"""
Process API response JSON data
Extracts clean responses and counts sources
Creates comparison CSVs for GTM analysis
"""

import json
import csv
import pandas as pd
from pathlib import Path
import argparse
from typing import Dict, List, Any


def extract_clean_answer(api_name: str, response_data: Dict) -> tuple:
    """Extract answer and sources from response based on API format"""
    answer = ""
    sources = []

    # Handle None response_data
    if response_data is None:
        return answer, sources

    # Handle different API response formats
    if api_name in ["you", "tavily", "perplexity"]:
        answer = response_data.get("answer", "")
        sources = response_data.get("sources", [])
    elif api_name in ["parallel_agentic", "parallel_oneshot"]:
        answer = response_data.get("answer", response_data.get("content", ""))
        sources = response_data.get("sources", [])
    elif api_name in ["linkup_standard", "linkup_deep"]:
        answer = response_data.get("content", response_data.get("answer", ""))
        sources = response_data.get("sources", [])
    elif api_name in ["exa", "valyu"]:
        answer = response_data.get("answer", response_data.get("content", ""))
        sources = response_data.get("sources", [])
    else:
        # Generic fallback
        answer = response_data.get("answer", "") or response_data.get("content", "")
        sources = response_data.get("sources", [])

    return answer, sources


def process_benchmark_data(json_data: List[Dict]) -> List[Dict]:
    """Process the benchmark JSON data structure"""
    results = []

    for item in json_data:
        query = item.get("query", "")
        responses = item.get("responses", [])

        for response in responses:
            api_name = response.get("api_name", "")
            response_data = response.get("response_data", {})

            # Extract answer and sources
            answer, sources = extract_clean_answer(api_name, response_data)

            # Count sources
            source_count = len(sources) if isinstance(sources, list) else 0

            # Extract source URLs if available
            source_urls = []
            if isinstance(sources, list):
                for source in sources:
                    if isinstance(source, dict) and "url" in source:
                        source_urls.append(source["url"])
                    elif isinstance(source, str):
                        source_urls.append(source)

            # Clean answer (remove excessive whitespace)
            if answer:
                answer = " ".join(answer.split())
                answer_preview = answer[:500] + "..." if len(answer) > 500 else answer
            else:
                answer_preview = ""

            results.append({
                "query": query,
                "api_name": api_name,
                "answer_preview": answer_preview,
                "full_answer": answer,
                "source_count": source_count,
                "source_urls": "; ".join(source_urls),
                "response_time": response.get("response_time", 0),
                "success": response.get("success", False),
                "timestamp": response.get("timestamp", ""),
                "word_count": len(answer.split()) if answer else 0
            })

    return results


def create_comparison_csv(results: List[Dict], output_dir: Path):
    """Create side-by-side comparison CSV"""
    comparison_data = {}

    for result in results:
        query = result['query']
        api = result['api_name']

        if query not in comparison_data:
            comparison_data[query] = {'query': query}

        comparison_data[query][f'{api}_answer'] = result['full_answer']
        comparison_data[query][f'{api}_sources'] = result['source_count']
        comparison_data[query][f'{api}_time'] = result['response_time']
        comparison_data[query][f'{api}_word_count'] = result['word_count']

    df_comparison = pd.DataFrame(list(comparison_data.values()))
    output_path = output_dir / 'api_comparison.csv'
    df_comparison.to_csv(output_path, index=False)
    print(f"  ✓ {output_path}")

    return df_comparison


def main():
    parser = argparse.ArgumentParser(
        description='Process API benchmark results and generate analysis CSVs'
    )
    parser.add_argument('input_file', help='Path to benchmark results JSON file')
    parser.add_argument('--output-dir', default='analysis_results',
                        help='Output directory for CSV files (default: analysis_results)')
    parser.add_argument('--create-comparison', action='store_true',
                        help='Create side-by-side comparison CSV')

    args = parser.parse_args()

    # Setup output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    print(f"\n{'='*80}")
    print("API RESPONSE PROCESSING")
    print(f"{'='*80}\n")

    # Load data
    print(f"Loading: {args.input_file}")
    with open(args.input_file, 'r') as f:
        data = json.load(f)

    if not isinstance(data, list):
        data = [data]

    # Process data
    print(f"Processing {len(data)} queries...")
    results = process_benchmark_data(data)

    # Save outputs
    print(f"\nGenerating reports in: {output_dir}/\n")

    # 1. Full responses CSV (clean answers without source listings)
    df_full = pd.DataFrame(results)
    df_full[['query', 'api_name', 'full_answer', 'source_count', 'word_count', 'response_time', 'success', 'timestamp']].to_csv(
        output_dir / 'clean_responses.csv', index=False
    )
    print(f"  ✓ {output_dir / 'clean_responses.csv'}")

    # 2. Statistics CSV (metrics only, no full text)
    df_stats = pd.DataFrame(results)
    df_stats[['query', 'api_name', 'source_count', 'word_count', 'response_time', 'success', 'timestamp']].to_csv(
        output_dir / 'response_statistics.csv', index=False
    )
    print(f"  ✓ {output_dir / 'response_statistics.csv'}")

    # 3. Comparison CSV (side-by-side)
    if args.create_comparison or True:  # Always create by default
        create_comparison_csv(results, output_dir)

    # Print summary
    print(f"\n{'='*80}")
    print("PROCESSING SUMMARY")
    print(f"{'='*80}\n")
    print(f"Total responses processed: {len(results)}")
    print(f"Unique queries: {len(set(r['query'] for r in results))}")

    # API statistics
    api_stats = {}
    for result in results:
        api = result['api_name']
        if api not in api_stats:
            api_stats[api] = {'count': 0, 'avg_sources': 0, 'avg_time': 0, 'avg_words': 0}
        api_stats[api]['count'] += 1
        api_stats[api]['avg_sources'] += result['source_count']
        api_stats[api]['avg_time'] += result['response_time']
        api_stats[api]['avg_words'] += result['word_count']

    print("\nAPI Statistics:")
    print(f"{'API':<20} {'Responses':<12} {'Avg Sources':<12} {'Avg Words':<12} {'Avg Time (s)':<12}")
    print("-" * 80)
    for api, stats in sorted(api_stats.items()):
        count = stats['count']
        print(f"{api:<20} {count:<12} {stats['avg_sources']/count:<12.1f} {stats['avg_words']/count:<12.0f} {stats['avg_time']/count:<12.2f}")

    print(f"\n{'='*80}")
    print("FILES CREATED")
    print(f"{'='*80}\n")
    print("  1. clean_responses.csv - Full responses without source listings")
    print("  2. response_statistics.csv - Metrics only (no full text)")
    print("  3. api_comparison.csv - Side-by-side comparison of APIs")
    print("\nNext step: Run quality_analyzer.py for competitive analysis")


if __name__ == "__main__":
    main()
