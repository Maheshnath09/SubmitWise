# Payment Integration Guide

## Overview

ProjectGen supports two payment providers:
- **Razorpay** - For Indian users (INR)
- **Stripe** - For global users (USD)

## Razorpay Integration (India)

### 1. Get API Keys

1. Sign up at https://razorpay.com
2. Go to Settings → API Keys
3. Generate Test/Live keys

### 2. Configure Environment

Add to `.env`:
```env
RAZORPAY_KEY_ID=rzp_test_xxxxx
RAZORPAY_KEY_SECRET=xxxxx
```

### 3. Update Backend Code

In `backend/app/api/payments.py`, uncomment:

```python
import razorpay

# In create_payment_order function:
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
order = client.order.create({
    "amount": int(amount * 100),  # Amount in paise
    "currency": "INR",
    "receipt": payment.id
})

payment.order_id = order['id']
db.commit()

return {
    "payment_id": payment.id,
    "provider": "razorpay",
    "order_id": order['id'],
    "key_id": settings.RAZORPAY_KEY_ID,
    "amount": amount
}
```

### 4. Frontend Integration

Install Razorpay SDK:
```bash
npm install razorpay
```

Create `frontend/components/payment/RazorpayCheckout.tsx`:

```typescript
'use client';

import { useEffect } from 'react';

declare global {
  interface Window {
    Razorpay: any;
  }
}

export default function RazorpayCheckout({ orderId, amount, onSuccess, onFailure }: any) {
  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://checkout.razorpay.com/v1/checkout.js';
    script.async = true;
    document.body.appendChild(script);
  }, []);

  const handlePayment = () => {
    const options = {
      key: process.env.NEXT_PUBLIC_RAZORPAY_KEY_ID,
      amount: amount * 100,
      currency: 'INR',
      order_id: orderId,
      name: 'ProjectGen',
      description: 'Credits Purchase',
      handler: function (response: any) {
        onSuccess(response);
      },
      prefill: {
        email: 'user@example.com',
      },
      theme: {
        color: '#8B5CF6'
      }
    };

    const razorpay = new window.Razorpay(options);
    razorpay.open();
  };

  return (
    <button onClick={handlePayment}>
      Pay with Razorpay
    </button>
  );
}
```

### 5. Webhook Setup

1. Go to Razorpay Dashboard → Webhooks
2. Add webhook URL: `https://yourdomain.com/api/payments/webhook`
3. Select events: `payment.captured`, `payment.failed`
4. Get webhook secret

Update webhook handler in `backend/app/api/payments.py`:

```python
import hmac
import hashlib

@router.post("/webhook")
async def payment_webhook(request: Request, db: Session = Depends(get_db)):
    body = await request.body()
    signature = request.headers.get('X-Razorpay-Signature')
    
    # Verify signature
    expected_signature = hmac.new(
        settings.RAZORPAY_WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    
    if signature != expected_signature:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    data = await request.json()
    event = data['event']
    
    if event == 'payment.captured':
        payment_id = data['payload']['payment']['entity']['notes']['payment_id']
        
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if payment:
            payment.status = 'completed'
            payment.transaction_id = data['payload']['payment']['entity']['id']
            payment.completed_at = datetime.utcnow()
            
            # Provision credits
            user = db.query(User).filter(User.id == payment.user_id).first()
            if user:
                user.credits += payment.credits_added
            
            db.commit()
    
    return {"status": "success"}
```

## Stripe Integration (Global)

### 1. Get API Keys

1. Sign up at https://stripe.com
2. Go to Developers → API Keys
3. Get Publishable and Secret keys

### 2. Configure Environment

Add to `.env`:
```env
STRIPE_SECRET_KEY=sk_test_xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_xxxxx
```

### 3. Install Stripe

Backend:
```bash
pip install stripe
```

Frontend:
```bash
npm install @stripe/stripe-js @stripe/react-stripe-js
```

### 4. Backend Implementation

In `backend/app/api/payments.py`:

```python
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

@router.post("/create-checkout-session")
async def create_checkout_session(
    credits: int,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    # Calculate amount
    amount = credits * 5  # $5 per credit
    
    # Create payment record
    payment = Payment(
        id=str(uuid.uuid4()),
        user_id=user_id,
        amount=amount,
        currency="USD",
        status="pending",
        provider="stripe",
        credits_added=credits
    )
    db.add(payment)
    db.commit()
    
    # Create Stripe checkout session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': f'{credits} ProjectGen Credits',
                },
                'unit_amount': amount * 100,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=f"{settings.FRONTEND_URL}/payment/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{settings.FRONTEND_URL}/payment/cancel",
        metadata={
            'payment_id': payment.id
        }
    )
    
    return {"session_id": session.id}
```

### 5. Frontend Stripe Checkout

Create `frontend/app/payment/page.tsx`:

```typescript
'use client';

import { loadStripe } from '@stripe/stripe-js';
import { paymentsAPI } from '@/lib/api';

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);

export default function PaymentPage() {
  const handleCheckout = async (credits: number) => {
    const stripe = await stripePromise;
    
    const response = await paymentsAPI.createCheckoutSession({ credits });
    const { session_id } = response.data;
    
    await stripe?.redirectToCheckout({ sessionId: session_id });
  };

  return (
    <div>
      <button onClick={() => handleCheckout(10)}>
        Buy 10 Credits - $50
      </button>
    </div>
  );
}
```

## Pricing Tiers

### Free Tier
- 2 projects/month
- All features
- Email support

### Pro Tier (₹299/month or $10/month)
- 20 projects/month
- Priority support
- Custom templates

### Enterprise
- Unlimited projects
- Bulk onboarding
- Dedicated support
- Custom pricing

## Testing

### Razorpay Test Cards
- Success: 4111 1111 1111 1111
- Failure: 4000 0000 0000 0002

### Stripe Test Cards
- Success: 4242 4242 4242 4242
- 3D Secure: 4000 0025 0000 3155
- Declined: 4000 0000 0000 0002

## Production Checklist

- [ ] Switch to live API keys
- [ ] Configure webhook URLs
- [ ] Test payment flow end-to-end
- [ ] Set up webhook monitoring
- [ ] Implement refund handling
- [ ] Add invoice generation
- [ ] Configure tax settings (if applicable)
- [ ] Test subscription renewals
- [ ] Set up payment failure notifications
