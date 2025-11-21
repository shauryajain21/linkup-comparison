"""Flask web application for API comparison interface."""
from flask import Flask, render_template, jsonify, request
from executor import QueryExecutor
from database import QueryDatabase, ResultsDatabase
from config import Config

app = Flask(__name__)
app.config['DEBUG'] = Config.DEBUG

# Initialize components
query_db = QueryDatabase()
results_db = ResultsDatabase()


@app.route('/')
def index():
    """Render main comparison interface."""
    return render_template('index.html')


@app.route('/api/queries')
def get_queries():
    """Get all available queries."""
    queries = query_db.get_all_queries()
    categories = query_db.get_categories()
    return jsonify({
        'queries': queries,
        'categories': categories
    })


@app.route('/api/execute', methods=['POST'])
def execute_queries():
    """Execute selected queries across APIs."""
    data = request.json
    query_ids = data.get('query_ids', [])
    api_names = data.get('api_names', None)

    try:
        executor = QueryExecutor()

        if not query_ids:
            # Execute all queries
            summary = executor.execute_from_database(
                api_names=api_names,
                save=True
            )
        else:
            # Execute specific queries
            summary = executor.execute_from_database(
                query_ids=query_ids,
                api_names=api_names,
                save=True
            )

        return jsonify({
            'success': True,
            'summary': {
                'total_queries': summary['total_queries'],
                'total_responses': summary['total_responses'],
                'total_time': summary['total_time'],
                'apis_used': summary['apis_used'],
                'successful': summary['successful'],
                'failed': summary['failed']
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/results')
def get_results():
    """Get latest results or specific run results."""
    run_id = request.args.get('run_id', None)

    try:
        comparison_data = results_db.get_comparison_data(run_id)

        if not comparison_data:
            return jsonify({
                'success': False,
                'error': 'No results found'
            }), 404

        return jsonify({
            'success': True,
            'data': comparison_data
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/runs')
def list_runs():
    """List all available result runs."""
    try:
        runs = results_db.list_runs()
        return jsonify({
            'success': True,
            'runs': runs
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/available-apis')
def available_apis():
    """Get list of available APIs."""
    try:
        apis = Config.get_available_apis()
        return jsonify({
            'success': True,
            'apis': apis
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/browse')
def browse():
    """Render interactive query browser and comparison interface."""
    return render_template('browse.html')


@app.route('/api/benchmark-results')
def get_benchmark_results():
    """Get all benchmark results from CSV for browsing."""
    import pandas as pd
    import os

    try:
        csv_path = 'master_results_all_batches.csv'
        if not os.path.exists(csv_path):
            return jsonify({
                'success': False,
                'error': 'Benchmark results file not found'
            }), 404

        # Read CSV
        df = pd.read_csv(csv_path)

        # Convert to list of dictionaries for easier frontend consumption
        results = []
        apis = ['linkup_standard', 'linkup_deep', 'perplexity', 'exa', 'you', 'tavily', 'valyu']

        for idx, row in df.iterrows():
            query_result = {
                'query_num': int(row['query_num']),
                'query': row['query'],
                'query_length': int(row['query_length']),
                'apis': {}
            }

            # Extract data for each API
            for api in apis:
                query_result['apis'][api] = {
                    'success': bool(row.get(f'{api}_success', False)),
                    'response_time': float(row.get(f'{api}_response_time_s', 0)) if pd.notna(row.get(f'{api}_response_time_s')) else None,
                    'answer': str(row.get(f'{api}_answer', '')) if pd.notna(row.get(f'{api}_answer')) else '',
                    'num_sources': int(row.get(f'{api}_num_sources', 0)) if pd.notna(row.get(f'{api}_num_sources')) else 0,
                    'source_urls': str(row.get(f'{api}_source_urls', '')) if pd.notna(row.get(f'{api}_source_urls')) else '',
                    'error': str(row.get(f'{api}_error', '')) if pd.notna(row.get(f'{api}_error')) else None
                }

            results.append(query_result)

        return jsonify({
            'success': True,
            'total_queries': len(results),
            'queries': results
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/compare', methods=['POST'])
def compare_apis():
    """Execute queries across selected APIs and return results."""
    data = request.json
    apis = data.get('apis', [])
    queries = data.get('queries', [])

    if not apis:
        return jsonify({
            'success': False,
            'error': 'No APIs selected'
        }), 400

    if not queries:
        return jsonify({
            'success': False,
            'error': 'No queries provided'
        }), 400

    try:
        executor = QueryExecutor()

        # Execute queries and organize results by query
        results_by_query = []

        for query in queries:
            query_results = executor.execute_single_query(query, apis)
            results_by_query.append({
                'query': query,
                'responses': query_results
            })

        return jsonify({
            'success': True,
            'results': results_by_query
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    # Validate configuration
    try:
        Config.validate()
        print(f"Available APIs: {Config.get_available_apis()}")
        app.run(debug=Config.DEBUG, port=8080)
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please configure your API keys in .env file")
