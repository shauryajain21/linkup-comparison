
@app.route('/master_results_all_batches.csv')
def download_csv():
    """Serve the master CSV file."""
    from flask import send_file
    return send_file('master_results_all_batches.csv', 
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name='linkup_benchmark_results.csv')

if __name__ == '__main__':
    app.run(debug=True)
