#!/bin/bash

# ProjectGen Setup Script
# This script creates the .env file with your configuration

echo "🚀 ProjectGen Setup"
echo "==================="
echo ""

# Check if .env already exists
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists!"
    read -p "Do you want to overwrite it? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 1
    fi
fi

# Copy from example
cp .env.example .env

echo "✅ Created .env file from template"
echo ""

# Prompt for payment keys
echo "📝 Payment Configuration"
echo "========================"
echo ""
echo "Leave blank to skip (you can add these later)"
echo ""

read -p "Razorpay Key ID (from https://dashboard.razorpay.com/app/keys): " razorpay_id
read -p "Razorpay Key Secret: " razorpay_secret
read -p "Stripe Secret Key (from https://dashboard.stripe.com/apikeys): " stripe_key
read -p "Stripe Webhook Secret: " stripe_webhook

# Update .env file
if [ ! -z "$razorpay_id" ]; then
    sed -i "s/RAZORPAY_KEY_ID=.*/RAZORPAY_KEY_ID=$razorpay_id/" .env
    echo "✅ Razorpay Key ID configured"
fi

if [ ! -z "$razorpay_secret" ]; then
    sed -i "s/RAZORPAY_KEY_SECRET=.*/RAZORPAY_KEY_SECRET=$razorpay_secret/" .env
    echo "✅ Razorpay Secret configured"
fi

if [ ! -z "$stripe_key" ]; then
    sed -i "s/STRIPE_SECRET_KEY=.*/STRIPE_SECRET_KEY=$stripe_key/" .env
    echo "✅ Stripe Secret Key configured"
fi

if [ ! -z "$stripe_webhook" ]; then
    sed -i "s/STRIPE_WEBHOOK_SECRET=.*/STRIPE_WEBHOOK_SECRET=$stripe_webhook/" .env
    echo "✅ Stripe Webhook Secret configured"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Review .env file and update any remaining values"
echo "2. Run: docker-compose up --build"
echo "3. Access: http://localhost:3000"
echo ""
echo "For payment integration, see PAYMENT_INTEGRATION.md"
