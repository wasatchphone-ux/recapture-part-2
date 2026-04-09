from flask import Flask, render_template_string
import os

app = Flask(__name__)

# Base HTML template for all offers
BASE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - Recapture Fitness</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .container {
            max-width: 600px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
            margin: 20px;
        }
        
        .header {
            background: linear-gradient(45deg, #ff6b6b, #ee5a52);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: bold;
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px 30px;
            text-align: center;
        }
        
        .offer-badge {
            display: inline-block;
            background: {{ badge_color }};
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: bold;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 30px;
        }
        
        .offer-title {
            font-size: 2rem;
            color: #333;
            margin-bottom: 20px;
            font-weight: bold;
        }
        
        .offer-description {
            font-size: 1.1rem;
            color: #666;
            margin-bottom: 30px;
            line-height: 1.8;
        }
        
        .features {
            list-style: none;
            margin-bottom: 40px;
        }
        
        .features li {
            padding: 12px 0;
            font-size: 1.1rem;
            color: #555;
            border-bottom: 1px solid #eee;
        }
        
        .features li:before {
            content: "✓";
            color: #4CAF50;
            font-weight: bold;
            margin-right: 15px;
        }
        
        .cta-button {
            display: inline-block;
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            padding: 18px 40px;
            text-decoration: none;
            border-radius: 50px;
            font-size: 1.2rem;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 10px 25px rgba(76, 175, 80, 0.3);
            transition: all 0.3s ease;
        }
        
        .cta-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(76, 175, 80, 0.4);
        }
        
        .urgency {
            margin-top: 30px;
            padding: 20px;
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            border-radius: 5px;
        }
        
        .urgency p {
            color: #856404;
            font-weight: bold;
            margin: 0;
        }
        
        .footer {
            background: #f8f9fa;
            padding: 20px 30px;
            text-align: center;
            color: #666;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome Back!</h1>
            <p>Your fitness journey continues here</p>
        </div>
        
        <div class="content">
            <div class="offer-badge">{{ badge_text }}</div>
            <h2 class="offer-title">{{ offer_title }}</h2>
            <p class="offer-description">{{ offer_description }}</p>
            
            <ul class="features">
                {% for feature in features %}
                <li>{{ feature }}</li>
                {% endfor %}
            </ul>
            
            <a href="{{ cta_link }}" class="cta-button">{{ cta_text }}</a>
            
            <div class="urgency">
                <p>{{ urgency_text }}</p>
            </div>
        </div>
        
        <div class="footer">
            <p>Questions? Call us at (555) 123-4567 or email hello@recapturefitness.com</p>
        </div>
    </div>
</body>
</html>
'''

# Offer configurations
OFFERS = {
    'free_week': {
        'title': 'Free Week Trial + Discount',
        'badge_text': 'Limited Time',
        'badge_color': '#ff6b6b',
        'offer_title': 'Free Week Trial + 50% Off First Month',
        'offer_description': 'Experience our full facilities risk-free, then save big on your first month membership.',
        'features': [
            '7 days unlimited gym access',
            'Free fitness assessment',
            'Access to all group classes',
            '50% off your first month after trial',
            'No commitment during trial period'
        ],
        'cta_text': 'Start Free Trial',
        'cta_link': 'https://your-shopify-store.com/checkout?utm_source=email&utm_medium=recapture&utm_campaign=free_week&utm_content=variant_a',
        'urgency_text': '⏰ This offer expires in 48 hours - Limited spots available!'
    },
    'first_month_free': {
        'title': 'First Month Free',
        'badge_text': 'Best Value',
        'badge_color': '#4CAF50',
        'offer_title': 'First Month Completely FREE',
        'offer_description': 'Join our 1-year membership and get your first month absolutely free - no strings attached.',
        'features': [
            'First month 100% free',
            '12-month membership commitment',
            'Automatic monthly EFT payments',
            'Access to premium amenities',
            'Free personal training session'
        ],
        'cta_text': 'Get Free Month',
        'cta_link': 'https://your-shopify-store.com/checkout?utm_source=email&utm_medium=recapture&utm_campaign=first_month_free&utm_content=variant_b',
        'urgency_text': '🔥 Only 25 memberships available at this price!'
    },
    'discount': {
        'title': '25% Off 3 Months',
        'badge_text': 'Most Flexible',
        'badge_color': '#9c27b0',
        'offer_title': '25% Off Your First 3 Months',
        'offer_description': 'Get significant savings with complete flexibility - no long-term commitment required.',
        'features': [
            '25% discount for 3 full months',
            'Month-to-month flexibility',
            'Cancel anytime after 3 months',
            'All facility access included',
            'Guest pass privileges'
        ],
        'cta_text': 'Get 25% Off',
        'cta_link': 'https://your-shopify-store.com/checkout?utm_source=email&utm_medium=recapture&utm_campaign=discount_3month&utm_content=variant_c',
        'urgency_text': '💪 Join 500+ members who chose flexibility!'
    }
}

@app.route('/')
def index():
    """Landing page showing all available offers"""
    return '''
    <html>
    <head>
        <title>Recapture Fitness - Offer Variants</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            .offer-link { display: block; margin: 20px 0; padding: 20px; background: #f5f5f5; 
                         text-decoration: none; color: #333; border-radius: 8px; }
            .offer-link:hover { background: #e0e0e0; }
            h1 { color: #333; }
            h3 { color: #666; margin: 0 0 10px 0; }
            p { margin: 0; color: #888; }
        </style>
    </head>
    <body>
        <h1>🏋️ Recapture Fitness - A/B Test Offers</h1>
        <p>Choose an offer variant to preview:</p>
        
        <a href="/offer_free_week.html" class="offer-link">
            <h3>Variant A: Free Week Trial + Discount</h3>
            <p>7-day trial + 50% off first month</p>
        </a>
        
        <a href="/offer_first_month_free.html" class="offer-link">
            <h3>Variant B: First Month Free</h3>
            <p>Free first month + 1-year commitment</p>
        </a>
        
        <a href="/offer_discount.html" class="offer-link">
            <h3>Variant C: 25% Off 3 Months</h3>
            <p>25% discount + month-to-month flexibility</p>
        </a>
        
        <hr style="margin: 40px 0;">
        <p><strong>For A/B Testing:</strong> Each offer has unique UTM parameters for Shopify tracking.</p>
        <p><strong>Next Steps:</strong> Send equal traffic to each variant and measure conversion rates.</p>
    </body>
    </html>
    '''

@app.route('/offer_free_week.html')
def offer_free_week():
    """Free week trial offer page"""
    offer = OFFERS['free_week']
    return render_template_string(BASE_TEMPLATE, **offer)

@app.route('/offer_first_month_free.html')
def offer_first_month_free():
    """First month free offer page"""
    offer = OFFERS['first_month_free']
    return render_template_string(BASE_TEMPLATE, **offer)

@app.route('/offer_discount.html')
def offer_discount():
    """25% discount offer page"""
    offer = OFFERS['discount']
    return render_template_string(BASE_TEMPLATE, **offer)

@app.route('/generate_files')
def generate_static_files():
    """Generate static HTML files for deployment"""
    try:
        # Create output directory
        if not os.path.exists('generated_offers'):
            os.makedirs('generated_offers')
        
        # Generate each offer as a static HTML file
        for offer_key, offer_data in OFFERS.items():
            filename = f"offer_{offer_key}.html"
            filepath = os.path.join('generated_offers', filename)
            
            # Render template with offer data
            html_content = render_template_string(BASE_TEMPLATE, **offer_data)
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
        
        return f'''
        <html>
        <body style="font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px;">
            <h2>✅ Static HTML Files Generated!</h2>
            <p>The following files have been created in the 'generated_offers' folder:</p>
            <ul>
                <li><strong>offer_free_week.html</strong> - Variant A (UTM: variant_a)</li>
                <li><strong>offer_first_month_free.html</strong> - Variant B (UTM: variant_b)</li>
                <li><strong>offer_discount.html</strong> - Variant C (UTM: variant_c)</li>
            </ul>
            <p>You can now upload these files to your web server or CDN for A/B testing.</p>
            <p><a href="/">← Back to preview</a></p>
        </body>
        </html>
        '''
    except Exception as e:
        return f"Error generating files: {str(e)}"

if __name__ == '__main__':
    print("🏋️ Recapture Fitness Offer Variants")
    print("=" * 40)
    print("Preview offers: http://localhost:5001")
    print("Generate static files: http://localhost:5001/generate_files")
    print("=" * 40)
    
    app.run(debug=True, port=5001)
===CODE===