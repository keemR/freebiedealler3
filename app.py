
from flask import Flask, render_template, request, jsonify
import json
from math import ceil
from collections import Counter

app = Flask(__name__)

# Load dummy data (in a real scenario, this would be a database)
with open('data.json', 'r') as f:
    deals_data = json.load(f)

ITEMS_PER_PAGE = 10
search_analytics = Counter()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    category = request.args.get('category', '').lower()
    page = int(request.args.get('page', 1))
    
    results = [deal for deal in deals_data if query in deal['title'].lower() or query in deal['description'].lower()]
    
    if category:
        results = [deal for deal in results if deal['category'].lower() == category]
    
    total_pages = ceil(len(results) / ITEMS_PER_PAGE)
    paginated_results = results[(page - 1) * ITEMS_PER_PAGE: page * ITEMS_PER_PAGE]
    search_analytics[query] += 1
    
    categories = sorted(set(deal['category'] for deal in deals_data))
    
    return render_template('search.html', results=paginated_results, query=query, category=category, page=page, total_pages=total_pages, categories=categories)

@app.route('/api/search')
def api_search():
    query = request.args.get('q', '').lower()
    page = int(request.args.get('page', 1))
    results = [deal for deal in deals_data if query in deal['title'].lower() or query in deal['description'].lower()]
    total_pages = ceil(len(results) / ITEMS_PER_PAGE)
    paginated_results = results[(page - 1) * ITEMS_PER_PAGE: page * ITEMS_PER_PAGE]
    search_analytics[query] += 1
    return jsonify({
        'results': paginated_results,
        'total_pages': total_pages,
        'current_page': page
    })

@app.route('/analytics')
def analytics():
    return render_template('analytics.html', search_analytics=search_analytics.most_common(10))

if __name__ == '__main__':
    app.run(debug=True)
