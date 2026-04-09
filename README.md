# Recapture Fitness - A/B Test Offer Variants

A Flask web application that generates three different fitness membership offer variants for A/B testing conversion rates before sending to 8,000 email contacts.

## Features

- **3 Offer Variants:**
  - **Variant A**: Free week trial + 50% off first month
  - **Variant B**: First month free + 1-year commitment  
  - **Variant C**: 25% off first 3 months, month-to-month

- **Unique UTM Tracking**: Each offer has distinct UTM parameters for Shopify conversion tracking
- **Professional Design**: Responsive, conversion-optimized landing pages
- **Static File Generation**: Create standalone HTML files for deployment

## Quick Start

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **Preview offers:**
   - Open http://localhost:5001
   - Click each variant to preview the offer pages

3. **Generate static files:**
   - Visit http://localhost:5001/generate_files
   - HTML files will be created in `generated_offers/` folder

## A/B Testing Setup

1. **Deploy the generated HTML files** to your web server/CDN
2. **Split your email list** into 3 equal segments (≈2,667 contacts each)
3. **Send each segment** to a different offer variant:
   - Segment 1 → `offer_free_week.html`
   - Segment 2 → `offer_first_month_free.html` 
   - Segment 3 → `offer_discount.html`

4. **Track conversions** in Shopify using the UTM parameters:
   - `utm_content=variant_a` (Free week trial)
   - `utm_content=variant_b` (First month free)
   - `utm_content=variant_c` (25% discount)

## UTM Tracking Parameters

Each CTA button includes complete tracking:
- `utm_source=email`
- `utm_medium=recapture` 
- `utm_campaign=[offer_type]`
- `utm_content=variant_[a|b|c]`

## Customization

Edit the `OFFERS` dictionary in `main.py` to:
- Change offer details and pricing
- Update your Shopify store URL
- Modify UTM parameters
- Adjust colors and styling

## Files Generated

- `offer_free_week.html` - Variant A
- `offer_first_month_free.html` - Variant B  
- `offer_discount.html` - Variant C

Ready for A/B testing to determine which offer converts best!
===README===