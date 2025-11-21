"""Database and storage management."""
import json
import os
from datetime import datetime
from typing import List, Dict, Any
from config import Config


class QueryDatabase:
    """Manager for query database."""

    def __init__(self, queries_file: str = "queries.json"):
        self.queries_file = queries_file
        self.queries = self._load_queries()

    def _load_queries(self) -> List[Dict]:
        """Load queries from JSON file."""
        if not os.path.exists(self.queries_file):
            return []

        with open(self.queries_file, 'r') as f:
            return json.load(f)

    def get_all_queries(self) -> List[Dict]:
        """Get all queries."""
        return self.queries

    def get_query_by_id(self, query_id: int) -> Dict:
        """Get a specific query by ID."""
        for query in self.queries:
            if query['id'] == query_id:
                return query
        return None

    def get_queries_by_category(self, category: str) -> List[Dict]:
        """Get queries filtered by category."""
        return [q for q in self.queries if q['category'] == category]

    def get_categories(self) -> List[str]:
        """Get list of unique categories."""
        return list(set(q['category'] for q in self.queries))


class ResultsDatabase:
    """Manager for storing and retrieving API results."""

    def __init__(self, results_dir: str = None):
        # Use /tmp in serverless environments (Vercel, AWS Lambda, etc.)
        if results_dir is None:
            results_dir = '/tmp/data' if os.getenv('VERCEL') else Config.RESULTS_DIR
        self.results_dir = results_dir
        os.makedirs(self.results_dir, exist_ok=True)

    def save_results(self, results: List[Dict], run_id: str = None) -> str:
        """
        Save API results to JSON file.

        Args:
            results: List of API response dictionaries
            run_id: Optional run ID, will generate timestamp-based if not provided

        Returns:
            Path to saved results file
        """
        if not run_id:
            run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = f"results_{run_id}.json"
        filepath = os.path.join(self.results_dir, filename)

        data = {
            'run_id': run_id,
            'timestamp': datetime.now().isoformat(),
            'total_queries': len(set(r['query'] for r in results)),
            'total_responses': len(results),
            'results': results
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        return filepath

    def load_results(self, run_id: str = None) -> Dict:
        """
        Load results from file.

        Args:
            run_id: Run ID to load. If None, loads most recent.

        Returns:
            Dictionary containing results data
        """
        if run_id:
            filename = f"results_{run_id}.json"
            filepath = os.path.join(self.results_dir, filename)
        else:
            # Get most recent results file
            files = [f for f in os.listdir(self.results_dir) if f.startswith('results_') and f.endswith('.json')]
            if not files:
                return None
            files.sort(reverse=True)
            filepath = os.path.join(self.results_dir, files[0])

        if not os.path.exists(filepath):
            return None

        with open(filepath, 'r') as f:
            return json.load(f)

    def list_runs(self) -> List[Dict]:
        """List all available result runs."""
        files = [f for f in os.listdir(self.results_dir) if f.startswith('results_') and f.endswith('.json')]
        runs = []

        for filename in sorted(files, reverse=True):
            filepath = os.path.join(self.results_dir, filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
                runs.append({
                    'run_id': data['run_id'],
                    'timestamp': data['timestamp'],
                    'total_queries': data['total_queries'],
                    'total_responses': data['total_responses']
                })

        return runs

    def get_comparison_data(self, run_id: str = None) -> Dict:
        """
        Get formatted comparison data for UI display.

        Args:
            run_id: Run ID to load

        Returns:
            Dictionary with queries and grouped API responses
        """
        data = self.load_results(run_id)
        if not data:
            return None

        # Group results by query
        comparison = {}
        for result in data['results']:
            query = result['query']
            if query not in comparison:
                comparison[query] = {
                    'query': query,
                    'responses': []
                }
            comparison[query]['responses'].append(result)

        return {
            'run_id': data['run_id'],
            'timestamp': data['timestamp'],
            'comparisons': list(comparison.values())
        }
