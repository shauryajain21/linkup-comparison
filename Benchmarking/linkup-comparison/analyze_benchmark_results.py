#!/usr/bin/env python3
"""
Comprehensive Benchmark Analysis Script
Analyzes the master_results_all_batches.csv to generate key insights
"""

import pandas as pd
import numpy as np
import json
from collections import defaultdict
from datetime import datetime
import os

# Configuration
CSV_FILE = "master_results_all_batches.csv"
OUTPUT_DIR = "analysis_output"
APIS = ['linkup_standard', 'linkup_deep', 'perplexity', 'exa', 'you', 'tavily', 'valyu']
API_DISPLAY_NAMES = {
    'linkup_standard': 'Linkup Standard',
    'linkup_deep': 'Linkup Deep',
    'perplexity': 'Perplexity',
    'exa': 'Exa',
    'you': 'You.com',
    'tavily': 'Tavily',
    'valyu': 'Valyu'
}


class BenchmarkAnalyzer:
    """Main analyzer class for benchmark results"""

    def __init__(self, csv_path):
        print(f"Loading data from {csv_path}...")
        self.df = pd.read_csv(csv_path)
        self.insights = {}
        self.apis = APIS

        # Create output directory
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        print(f"Loaded {len(self.df)} queries")
        print(f"Analyzing {len(self.apis)} APIs: {', '.join(self.apis)}")

    def run_full_analysis(self):
        """Run all analyses"""
        print("\n" + "="*80)
        print("STARTING COMPREHENSIVE BENCHMARK ANALYSIS")
        print("="*80 + "\n")

        self.analyze_performance_rankings()
        self.analyze_speed_vs_quality()
        self.analyze_by_category()
        self.analyze_failures()
        self.analyze_sources()
        self.analyze_query_complexity()
        self.competitive_positioning()

        # Generate outputs
        self.generate_markdown_report()
        self.generate_json_insights()

        print("\n" + "="*80)
        print("ANALYSIS COMPLETE!")
        print("="*80)
        print(f"\nOutputs saved to: {OUTPUT_DIR}/")
        print(f"  - analysis_report.md")
        print(f"  - insights_summary.json")
        print(f"  - recommendations.txt")

    def analyze_performance_rankings(self):
        """Analyze overall performance metrics"""
        print("\n📊 ANALYZING PERFORMANCE RANKINGS...")

        results = {}

        for api in self.apis:
            success_col = f'{api}_success'
            time_col = f'{api}_response_time_s'
            answer_col = f'{api}_answer'
            sources_col = f'{api}_num_sources'
            error_col = f'{api}_error'

            # Calculate metrics
            total_queries = len(self.df)
            successes = self.df[success_col].sum()
            success_rate = (successes / total_queries) * 100

            # Response time stats (only for successful queries)
            successful_times = self.df[self.df[success_col] == True][time_col]

            # Count timeouts
            timeouts = self.df[error_col].fillna('').str.contains('timed out|timeout', case=False, na=False).sum()

            # Answer length stats
            answer_lengths = self.df[self.df[success_col] == True][answer_col].fillna('').str.len()

            # Source count stats
            source_counts = self.df[self.df[success_col] == True][sources_col].fillna(0)

            results[api] = {
                'total_queries': total_queries,
                'successes': int(successes),
                'success_rate': round(success_rate, 2),
                'timeouts': int(timeouts),
                'avg_response_time': round(successful_times.mean(), 2) if len(successful_times) > 0 else None,
                'median_response_time': round(successful_times.median(), 2) if len(successful_times) > 0 else None,
                'p95_response_time': round(successful_times.quantile(0.95), 2) if len(successful_times) > 0 else None,
                'p99_response_time': round(successful_times.quantile(0.99), 2) if len(successful_times) > 0 else None,
                'avg_answer_length': round(answer_lengths.mean(), 0) if len(answer_lengths) > 0 else 0,
                'avg_sources': round(source_counts.mean(), 1) if len(source_counts) > 0 else 0
            }

        self.insights['performance_rankings'] = results

        # Print summary
        print("\n✅ Performance Rankings (by Success Rate):")
        sorted_apis = sorted(results.items(), key=lambda x: x[1]['success_rate'], reverse=True)
        for api, metrics in sorted_apis:
            print(f"  {API_DISPLAY_NAMES[api]:20s}: {metrics['success_rate']:5.1f}% success | "
                  f"{metrics['avg_response_time']:5.2f}s avg | {metrics['avg_sources']:4.1f} sources")

    def analyze_speed_vs_quality(self):
        """Analyze the trade-off between speed and quality"""
        print("\n⚡ ANALYZING SPEED VS QUALITY TRADE-OFFS...")

        results = {}

        for api in self.apis:
            success_col = f'{api}_success'
            time_col = f'{api}_response_time_s'
            answer_col = f'{api}_answer'
            sources_col = f'{api}_num_sources'

            # Get successful queries only
            successful = self.df[self.df[success_col] == True]

            if len(successful) > 0:
                avg_time = successful[time_col].mean()
                avg_answer_length = successful[answer_col].fillna('').str.len().mean()
                avg_sources = successful[sources_col].fillna(0).mean()

                # Calculate "quality per second" metrics
                chars_per_second = avg_answer_length / avg_time if avg_time > 0 else 0
                sources_per_second = avg_sources / avg_time if avg_time > 0 else 0

                results[api] = {
                    'avg_response_time': round(avg_time, 2),
                    'avg_answer_length': round(avg_answer_length, 0),
                    'avg_sources': round(avg_sources, 1),
                    'chars_per_second': round(chars_per_second, 1),
                    'sources_per_second': round(sources_per_second, 2)
                }

        self.insights['speed_vs_quality'] = results

        # Print top performers
        print("\n🏆 Best Value (Characters per Second):")
        sorted_by_value = sorted(results.items(), key=lambda x: x[1]['chars_per_second'], reverse=True)
        for i, (api, metrics) in enumerate(sorted_by_value[:3], 1):
            print(f"  {i}. {API_DISPLAY_NAMES[api]:20s}: {metrics['chars_per_second']:6.1f} chars/sec "
                  f"({metrics['avg_answer_length']:.0f} chars in {metrics['avg_response_time']:.2f}s)")

    def analyze_by_category(self):
        """Analyze performance by query category if available"""
        print("\n📁 ANALYZING BY QUERY CATEGORY...")

        # Try to infer categories from query content
        def categorize_query(query_text):
            query_lower = str(query_text).lower()

            if 'linkedin' in query_lower or 'ceo' in query_lower or 'founder' in query_lower:
                return 'Company/LinkedIn Research'
            elif any(word in query_lower for word in ['what is', 'who is', 'when was', 'where is', 'how to']):
                return 'Q&A/Informational'
            elif 'summarize' in query_lower or 'summary of' in query_lower:
                return 'Summarization'
            elif len(query_lower) < 50:
                return 'Short Query'
            elif len(query_lower) > 500:
                return 'Long/Complex Query'
            else:
                return 'General Search'

        # Add category column
        self.df['category'] = self.df['query'].apply(categorize_query)

        # Analyze performance by category
        categories = self.df['category'].unique()
        results = {}

        for category in categories:
            cat_df = self.df[self.df['category'] == category]
            cat_results = {}

            for api in self.apis:
                success_col = f'{api}_success'
                success_rate = (cat_df[success_col].sum() / len(cat_df)) * 100
                cat_results[api] = {
                    'query_count': len(cat_df),
                    'success_rate': round(success_rate, 1)
                }

            results[category] = cat_results

        self.insights['category_analysis'] = results

        # Print category winners
        print("\n🎯 Category Winners:")
        for category in sorted(results.keys()):
            cat_data = results[category]
            winner = max(cat_data.items(), key=lambda x: x[1]['success_rate'])
            query_count = winner[1]['query_count']
            print(f"  {category:30s}: {API_DISPLAY_NAMES[winner[0]]:20s} ({winner[1]['success_rate']:.1f}% | {query_count} queries)")

    def analyze_failures(self):
        """Analyze failure patterns and timeouts"""
        print("\n❌ ANALYZING FAILURES AND TIMEOUTS...")

        results = {}

        for api in self.apis:
            success_col = f'{api}_success'
            error_col = f'{api}_error'

            failures = self.df[self.df[success_col] == False]

            # Count error types
            errors = failures[error_col].fillna('Unknown')
            timeout_count = errors.str.contains('timed out|timeout', case=False, na=False).sum()
            other_errors = len(failures) - timeout_count

            results[api] = {
                'total_failures': len(failures),
                'timeouts': int(timeout_count),
                'other_errors': int(other_errors),
                'timeout_rate': round((timeout_count / len(self.df)) * 100, 2) if len(self.df) > 0 else 0
            }

        self.insights['failure_analysis'] = results

        # Print timeout leaders (problems)
        print("\n⏰ APIs with Most Timeouts:")
        sorted_timeouts = sorted(results.items(), key=lambda x: x[1]['timeout_rate'], reverse=True)
        for api, metrics in sorted_timeouts[:5]:
            if metrics['timeout_rate'] > 0:
                print(f"  {API_DISPLAY_NAMES[api]:20s}: {metrics['timeouts']:4d} timeouts ({metrics['timeout_rate']:5.2f}% of all queries)")

    def analyze_sources(self):
        """Analyze source citation patterns"""
        print("\n📚 ANALYZING SOURCE CITATIONS...")

        results = {}

        for api in self.apis:
            success_col = f'{api}_success'
            sources_col = f'{api}_num_sources'
            answer_col = f'{api}_answer'

            successful = self.df[self.df[success_col] == True]

            if len(successful) > 0:
                source_counts = successful[sources_col].fillna(0)
                answer_lengths = successful[answer_col].fillna('').str.len()

                # Calculate correlation between sources and answer length
                correlation = source_counts.corr(answer_lengths) if len(source_counts) > 1 else 0

                results[api] = {
                    'avg_sources': round(source_counts.mean(), 1),
                    'median_sources': int(source_counts.median()),
                    'max_sources': int(source_counts.max()),
                    'min_sources': int(source_counts.min()),
                    'source_answer_correlation': round(correlation, 3)
                }

        self.insights['source_analysis'] = results

        # Print source depth leaders
        print("\n🔍 Source Depth Leaders:")
        sorted_sources = sorted(results.items(), key=lambda x: x[1]['avg_sources'], reverse=True)
        for api, metrics in sorted_sources[:5]:
            print(f"  {API_DISPLAY_NAMES[api]:20s}: {metrics['avg_sources']:5.1f} avg sources | "
                  f"Correlation with answer length: {metrics['source_answer_correlation']:5.3f}")

    def analyze_query_complexity(self):
        """Analyze performance across different query complexities"""
        print("\n🔤 ANALYZING QUERY COMPLEXITY IMPACT...")

        # Define query complexity buckets
        self.df['query_complexity'] = pd.cut(
            self.df['query_length'],
            bins=[0, 50, 200, 500, float('inf')],
            labels=['Very Short (<50)', 'Short (50-200)', 'Medium (200-500)', 'Long (500+)']
        )

        results = {}

        for complexity in self.df['query_complexity'].cat.categories:
            complex_df = self.df[self.df['query_complexity'] == complexity]
            complex_results = {}

            for api in self.apis:
                success_col = f'{api}_success'
                time_col = f'{api}_response_time_s'

                if len(complex_df) > 0:
                    success_rate = (complex_df[success_col].sum() / len(complex_df)) * 100
                    avg_time = complex_df[complex_df[success_col] == True][time_col].mean()

                    complex_results[api] = {
                        'query_count': len(complex_df),
                        'success_rate': round(success_rate, 1),
                        'avg_response_time': round(avg_time, 2) if not pd.isna(avg_time) else None
                    }

            results[str(complexity)] = complex_results

        self.insights['complexity_analysis'] = results

        # Print insights
        print("\n📊 Performance by Query Complexity:")
        for complexity, data in results.items():
            query_count = data[self.apis[0]]['query_count']
            print(f"\n  {complexity} ({query_count} queries):")
            sorted_apis = sorted(data.items(), key=lambda x: x[1]['success_rate'], reverse=True)
            for api, metrics in sorted_apis[:3]:
                print(f"    {API_DISPLAY_NAMES[api]:20s}: {metrics['success_rate']:5.1f}% success | "
                      f"{metrics['avg_response_time'] if metrics['avg_response_time'] else 0:5.2f}s avg")

    def competitive_positioning(self):
        """Analyze competitive positioning for Linkup"""
        print("\n🎯 ANALYZING COMPETITIVE POSITIONING...")

        linkup_std = self.insights['performance_rankings']['linkup_standard']
        linkup_deep = self.insights['performance_rankings']['linkup_deep']

        # Compare with each competitor
        competitors = [api for api in self.apis if 'linkup' not in api]

        positioning = {
            'linkup_standard': {
                'strengths': [],
                'weaknesses': [],
                'recommendations': []
            },
            'linkup_deep': {
                'strengths': [],
                'weaknesses': [],
                'recommendations': []
            }
        }

        # Analyze strengths and weaknesses
        for linkup_variant, linkup_data in [('linkup_standard', linkup_std), ('linkup_deep', linkup_deep)]:
            for competitor in competitors:
                comp_data = self.insights['performance_rankings'][competitor]

                # Compare key metrics
                if linkup_data['avg_sources'] > comp_data['avg_sources'] * 1.5:
                    positioning[linkup_variant]['strengths'].append(
                        f"Significantly more sources than {API_DISPLAY_NAMES[competitor]} "
                        f"({linkup_data['avg_sources']:.1f} vs {comp_data['avg_sources']:.1f})"
                    )

                if linkup_data['success_rate'] < comp_data['success_rate']:
                    positioning[linkup_variant]['weaknesses'].append(
                        f"Lower success rate than {API_DISPLAY_NAMES[competitor]} "
                        f"({linkup_data['success_rate']:.1f}% vs {comp_data['success_rate']:.1f}%)"
                    )

                if linkup_data['avg_response_time'] > comp_data['avg_response_time'] * 1.5:
                    positioning[linkup_variant]['weaknesses'].append(
                        f"Significantly slower than {API_DISPLAY_NAMES[competitor]} "
                        f"({linkup_data['avg_response_time']:.2f}s vs {comp_data['avg_response_time']:.2f}s)"
                    )

        # Add specific recommendations
        if linkup_deep['timeouts'] > 100:
            positioning['linkup_deep']['recommendations'].append(
                f"CRITICAL: Reduce timeout rate from {linkup_deep['timeouts']} timeouts "
                f"({(linkup_deep['timeouts']/linkup_deep['total_queries']*100):.1f}% of queries)"
            )

        self.insights['competitive_positioning'] = positioning

        # Print positioning
        print("\n💪 Linkup Standard Strengths:")
        for strength in positioning['linkup_standard']['strengths'][:5]:
            print(f"  ✓ {strength}")

        print("\n⚠️  Linkup Standard Areas for Improvement:")
        for weakness in positioning['linkup_standard']['weaknesses'][:5]:
            print(f"  • {weakness}")

        print("\n💪 Linkup Deep Strengths:")
        for strength in positioning['linkup_deep']['strengths'][:5]:
            print(f"  ✓ {strength}")

        print("\n⚠️  Linkup Deep Critical Issues:")
        for rec in positioning['linkup_deep']['recommendations']:
            print(f"  ⚡ {rec}")

    def generate_markdown_report(self):
        """Generate comprehensive markdown report"""
        print("\n📝 Generating markdown report...")

        report_path = os.path.join(OUTPUT_DIR, 'analysis_report.md')

        with open(report_path, 'w') as f:
            f.write("# Benchmark Analysis Report\n\n")
            f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            f.write(f"**Dataset**: {len(self.df)} queries across {len(self.apis)} APIs\n\n")

            f.write("---\n\n")

            # Performance Rankings
            f.write("## 1. Performance Rankings\n\n")
            f.write("| API | Success Rate | Avg Time | P95 Time | Avg Sources | Avg Answer Length |\n")
            f.write("|-----|--------------|----------|----------|-------------|-------------------|\n")

            perf = self.insights['performance_rankings']
            sorted_apis = sorted(perf.items(), key=lambda x: x[1]['success_rate'], reverse=True)
            for api, metrics in sorted_apis:
                f.write(f"| {API_DISPLAY_NAMES[api]} | "
                       f"{metrics['success_rate']:.1f}% | "
                       f"{metrics['avg_response_time']:.2f}s | "
                       f"{metrics['p95_response_time']:.2f}s | "
                       f"{metrics['avg_sources']:.1f} | "
                       f"{metrics['avg_answer_length']:.0f} |\n")

            f.write("\n---\n\n")

            # Speed vs Quality
            f.write("## 2. Speed vs Quality Analysis\n\n")
            f.write("### Best Value (Characters per Second)\n\n")

            speed_quality = self.insights['speed_vs_quality']
            sorted_value = sorted(speed_quality.items(), key=lambda x: x[1]['chars_per_second'], reverse=True)

            for i, (api, metrics) in enumerate(sorted_value, 1):
                f.write(f"{i}. **{API_DISPLAY_NAMES[api]}**: {metrics['chars_per_second']:.1f} chars/sec\n")
                f.write(f"   - {metrics['avg_answer_length']:.0f} characters in {metrics['avg_response_time']:.2f}s\n")
                f.write(f"   - {metrics['sources_per_second']:.2f} sources per second\n\n")

            f.write("\n---\n\n")

            # Failure Analysis
            f.write("## 3. Reliability Analysis\n\n")
            f.write("### Timeout Rates\n\n")

            failures = self.insights['failure_analysis']
            sorted_timeouts = sorted(failures.items(), key=lambda x: x[1]['timeout_rate'], reverse=True)

            f.write("| API | Total Failures | Timeouts | Timeout Rate |\n")
            f.write("|-----|----------------|----------|-------------|\n")

            for api, metrics in sorted_timeouts:
                f.write(f"| {API_DISPLAY_NAMES[api]} | "
                       f"{metrics['total_failures']} | "
                       f"{metrics['timeouts']} | "
                       f"{metrics['timeout_rate']:.2f}% |\n")

            f.write("\n---\n\n")

            # Competitive Positioning
            f.write("## 4. Competitive Positioning (Linkup)\n\n")

            positioning = self.insights['competitive_positioning']

            f.write("### Linkup Standard\n\n")
            f.write("**Strengths:**\n")
            for strength in positioning['linkup_standard']['strengths']:
                f.write(f"- {strength}\n")

            f.write("\n**Areas for Improvement:**\n")
            for weakness in positioning['linkup_standard']['weaknesses']:
                f.write(f"- {weakness}\n")

            f.write("\n### Linkup Deep\n\n")
            f.write("**Strengths:**\n")
            for strength in positioning['linkup_deep']['strengths']:
                f.write(f"- {strength}\n")

            f.write("\n**Critical Issues:**\n")
            for rec in positioning['linkup_deep']['recommendations']:
                f.write(f"- ⚠️  {rec}\n")

            f.write("\n---\n\n")
            f.write("## 5. Recommendations\n\n")
            f.write(self._generate_recommendations())

        print(f"✅ Report saved to: {report_path}")

    def generate_json_insights(self):
        """Generate JSON output of all insights"""
        print("\n💾 Generating JSON insights...")

        json_path = os.path.join(OUTPUT_DIR, 'insights_summary.json')

        with open(json_path, 'w') as f:
            json.dump(self.insights, f, indent=2)

        print(f"✅ JSON saved to: {json_path}")

    def _generate_recommendations(self):
        """Generate actionable recommendations"""
        recommendations = []

        # Based on analysis
        perf = self.insights['performance_rankings']

        # Speed recommendations
        fastest = min(perf.items(), key=lambda x: x[1]['avg_response_time'] or float('inf'))
        recommendations.append(
            f"### For Speed-Critical Applications\n"
            f"Use **{API_DISPLAY_NAMES[fastest[0]]}** - fastest at {fastest[1]['avg_response_time']:.2f}s average\n"
        )

        # Reliability recommendations
        most_reliable = max(perf.items(), key=lambda x: x[1]['success_rate'])
        recommendations.append(
            f"### For Maximum Reliability\n"
            f"Use **{API_DISPLAY_NAMES[most_reliable[0]]}** - {most_reliable[1]['success_rate']:.1f}% success rate\n"
        )

        # Source depth
        most_sources = max(perf.items(), key=lambda x: x[1]['avg_sources'])
        recommendations.append(
            f"### For Comprehensive Research\n"
            f"Use **{API_DISPLAY_NAMES[most_sources[0]]}** - {most_sources[1]['avg_sources']:.1f} sources per query\n"
        )

        # Linkup-specific
        linkup_deep_timeouts = perf['linkup_deep']['timeouts']
        if linkup_deep_timeouts > 100:
            recommendations.append(
                f"### CRITICAL: Linkup Deep Optimization\n"
                f"- Reduce timeout rate (currently {linkup_deep_timeouts} timeouts)\n"
                f"- Consider implementing progressive timeout strategy\n"
                f"- May need infrastructure scaling\n"
            )

        return "\n".join(recommendations)


def main():
    """Main execution"""
    analyzer = BenchmarkAnalyzer(CSV_FILE)
    analyzer.run_full_analysis()

    print("\n" + "="*80)
    print("📊 QUICK SUMMARY")
    print("="*80)

    # Print quick wins
    perf = analyzer.insights['performance_rankings']

    print("\n🏆 Top Performers:")
    print(f"  Fastest: {API_DISPLAY_NAMES[min(perf.items(), key=lambda x: x[1]['avg_response_time'] or float('inf'))[0]]}")
    print(f"  Most Reliable: {API_DISPLAY_NAMES[max(perf.items(), key=lambda x: x[1]['success_rate'])[0]]}")
    print(f"  Most Sources: {API_DISPLAY_NAMES[max(perf.items(), key=lambda x: x[1]['avg_sources'])[0]]}")

    print(f"\n📁 Full report: {OUTPUT_DIR}/analysis_report.md")
    print(f"📊 Data: {OUTPUT_DIR}/insights_summary.json")


if __name__ == "__main__":
    main()
