from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "name": "Wireless Headphones", "price": 1499, "category": "Electronics"},
    {"id": 2, "name": "Running Shoes", "price": 2299, "category": "Fashion"},
    {"id": 3, "name": "Coffee Mug", "price": 299, "category": "Home"},
]

PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>eKart Mini Store</title>
  <style>
    body{font-family:Arial,sans-serif;background:#f4f6f9;margin:0;color:#172033}
    header{background:#172554;color:white;padding:24px 8%;display:flex;justify-content:space-between}
    main{max-width:950px;margin:40px auto;padding:0 18px}
    .products{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:18px}
    .card{background:white;padding:22px;border-radius:12px;box-shadow:0 3px 14px #0001}
    .price{font-size:22px;font-weight:bold;color:#0f766e}
    a{color:#2563eb}
    footer{text-align:center;padding:25px;color:#64748b}
  </style>
</head>
<body>
<header><strong>🛒 eKart</strong><span>Mini online store</span></header>
<main>
  <h1>Welcome to eKart</h1>
  <p>A small Flask app deployed on Red Hat OpenShift.</p>
  <div class="products">
  {% for p in products %}
    <section class="card">
      <h2>{{ p.name }}</h2><p>{{ p.category }}</p>
      <p class="price">₹{{ p.price }}</p>
    </section>
  {% endfor %}
  </div>
  <p>API: <a href="/api/products">/api/products</a> · Health: <a href="/health">/health</a></p>
</main>
<footer>eKart DevOps practice project</footer>
</body></html>
"""

@app.get("/")
def home():
    return render_template_string(PAGE, products=PRODUCTS)

@app.get("/api/products")
def products():
    return jsonify(PRODUCTS)

@app.get("/health")
def health():
    return jsonify(status="ok"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
