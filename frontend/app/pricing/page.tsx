'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Check, Loader2, Crown, ArrowLeft } from 'lucide-react';
import { paymentsAPI } from '@/lib/api';
import Link from 'next/link';

declare global {
    interface Window {
        Razorpay: any;
    }
}

const pricingPlans = [
    {
        id: 'free',
        name: 'Free',
        price: 0,
        displayPrice: '₹0',
        period: '/month',
        description: 'Perfect for trying out SubmitWise',
        features: [
            '2 projects per month',
            'All document types (DOCX, PPTX)',
            'Basic plagiarism check',
            'Email support',
        ],
        cta: 'Current Plan',
        highlighted: false,
    },
    {
        id: 'pro',
        name: 'Pro',
        price: 299,
        displayPrice: '₹299',
        period: '/month',
        description: 'Best for active students',
        features: [
            '20 projects per month',
            'All document types',
            'Advanced plagiarism detection',
            'Priority support',
            'Custom templates',
            'Hindi language support',
        ],
        cta: 'Upgrade to Pro',
        highlighted: true,
    },
    {
        id: 'enterprise',
        name: 'Enterprise',
        price: null,
        displayPrice: 'Custom',
        period: '',
        description: 'For colleges and institutions',
        features: [
            'Unlimited projects',
            'Bulk student onboarding',
            'College-specific templates',
            'Dedicated support',
            'Usage analytics',
            'API access',
        ],
        cta: 'Contact Sales',
        highlighted: false,
    },
];

export default function PricingPage() {
    const router = useRouter();
    const [loading, setLoading] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [currentPlan, setCurrentPlan] = useState<string>('free');
    const [credits, setCredits] = useState<number>(2);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        // Check if user is logged in
        const token = localStorage.getItem('access_token');
        if (!token) {
            router.push('/auth/login?redirect=/pricing');
            return;
        }
        setIsAuthenticated(true);

        // Fetch current subscription
        paymentsAPI.getSubscription()
            .then(response => {
                setCurrentPlan(response.data.subscription_tier || 'free');
                setCredits(response.data.credits || 2);
            })
            .catch(err => {
                console.error('Failed to fetch subscription:', err);
            });
    }, [router]);

    const loadRazorpayScript = (): Promise<boolean> => {
        return new Promise((resolve) => {
            if (window.Razorpay) {
                resolve(true);
                return;
            }
            const script = document.createElement('script');
            script.src = 'https://checkout.razorpay.com/v1/checkout.js';
            script.onload = () => resolve(true);
            script.onerror = () => resolve(false);
            document.body.appendChild(script);
        });
    };

    const handleUpgrade = async (planId: string) => {
        if (planId === 'enterprise') {
            window.open('mailto:support@projectgen.ai?subject=Enterprise Plan Inquiry', '_blank');
            return;
        }

        if (planId === 'free' || planId === currentPlan) {
            return;
        }

        setLoading(planId);
        setError(null);

        try {
            // Load Razorpay script
            const scriptLoaded = await loadRazorpayScript();
            if (!scriptLoaded) {
                throw new Error('Failed to load Razorpay SDK');
            }

            // Create order (stores pending payment in backend)
            const orderResponse = await paymentsAPI.createOrder(planId);
            const orderData = orderResponse.data;

            // Configure Razorpay options - NO order_id since we don't have server-side order creation
            const options = {
                key: process.env.NEXT_PUBLIC_RAZORPAY_KEY_ID,
                amount: orderData.amount,
                currency: orderData.currency,
                name: 'SubmitWise',
                description: `Upgrade to ${orderData.plan_name} Plan`,
                prefill: orderData.prefill,
                theme: {
                    color: '#7c3aed',
                },
                handler: async (response: any) => {
                    try {
                        // Verify payment with backend
                        const verifyResponse = await paymentsAPI.verifyPayment({
                            razorpay_payment_id: response.razorpay_payment_id,
                            razorpay_order_id: orderData.payment_id, // Use our internal payment ID
                            plan: planId,
                        });

                        if (verifyResponse.data.success) {
                            setCurrentPlan(planId);
                            setCredits(verifyResponse.data.credits);
                            alert(`🎉 ${verifyResponse.data.message}\nYou now have ${verifyResponse.data.credits} credits!`);
                            router.push('/dashboard');
                        }
                    } catch (err: any) {
                        setError('Payment verification failed. Please contact support.');
                    } finally {
                        setLoading(null);
                    }
                },
                modal: {
                    ondismiss: () => {
                        setLoading(null);
                    },
                },
            };

            // Open Razorpay checkout
            const rzp = new window.Razorpay(options);
            rzp.on('payment.failed', (response: any) => {
                setError(`Payment failed: ${response.error.description}`);
                setLoading(null);
            });
            rzp.open();

        } catch (err: any) {
            setError(err.response?.data?.detail || err.message || 'Something went wrong');
            setLoading(null);
        }
    };

    const getButtonText = (plan: typeof pricingPlans[0]) => {
        if (plan.id === currentPlan) {
            return 'Current Plan';
        }
        if (plan.id === 'enterprise') {
            return 'Contact Sales';
        }
        if (plan.id === 'free' && currentPlan !== 'free') {
            return 'Downgrade';
        }
        return plan.cta;
    };

    const isButtonDisabled = (plan: typeof pricingPlans[0]) => {
        return plan.id === currentPlan || plan.id === 'free' || loading === plan.id;
    };

    if (!isAuthenticated) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <Loader2 className="w-8 h-8 animate-spin text-purple-600" />
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 dark:from-gray-900 dark:via-purple-900/10 dark:to-gray-900 py-12 px-4">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="mb-8">
                    <Link href="/dashboard" className="inline-flex items-center text-purple-600 dark:text-purple-400 hover:underline mb-4">
                        <ArrowLeft className="w-4 h-4 mr-2" />
                        Back to Dashboard
                    </Link>
                </div>

                {/* Current Plan Info */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 mb-12"
                >
                    <div className="flex items-center justify-between flex-wrap gap-4">
                        <div>
                            <h2 className="text-2xl font-bold flex items-center gap-2">
                                <Crown className="w-6 h-6 text-yellow-500" />
                                Current Plan: <span className="text-purple-600 dark:text-purple-400 capitalize">{currentPlan}</span>
                            </h2>
                            <p className="text-gray-600 dark:text-gray-400 mt-1">
                                You have <span className="font-bold text-purple-600">{credits}</span> credits remaining this month
                            </p>
                        </div>
                    </div>
                </motion.div>

                {/* Pricing Header */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    className="text-center mb-16"
                >
                    <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-purple-600 to-blue-600 dark:from-purple-400 dark:to-blue-400">
                        Upgrade Your Plan
                    </h1>
                    <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
                        Get more credits and unlock premium features
                    </p>
                    {error && (
                        <div className="mt-4 p-4 bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 rounded-lg max-w-md mx-auto">
                            {error}
                        </div>
                    )}
                </motion.div>

                {/* Pricing Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {pricingPlans.map((plan, index) => (
                        <motion.div
                            key={plan.name}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, delay: 0.2 + index * 0.1 }}
                            className={plan.highlighted ? 'md:-mt-4' : ''}
                        >
                            <Card className={`h-full flex flex-col relative ${plan.highlighted
                                ? 'border-purple-500 dark:border-purple-400 shadow-xl scale-105'
                                : 'border-gray-200 dark:border-gray-700'
                                } ${plan.id === currentPlan ? 'ring-2 ring-green-500' : ''}`}>
                                {plan.id === currentPlan && (
                                    <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-green-500 text-white text-xs px-3 py-1 rounded-full font-semibold">
                                        Your Plan
                                    </div>
                                )}
                                {plan.highlighted && plan.id !== currentPlan && (
                                    <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white text-center py-2 rounded-t-lg font-semibold">
                                        Most Popular
                                    </div>
                                )}
                                <CardHeader>
                                    <CardTitle className="text-2xl">{plan.name}</CardTitle>
                                    <CardDescription>{plan.description}</CardDescription>
                                    <div className="mt-4">
                                        <span className="text-4xl font-bold">{plan.displayPrice}</span>
                                        <span className="text-gray-600 dark:text-gray-400">{plan.period}</span>
                                    </div>
                                </CardHeader>
                                <CardContent className="flex-grow">
                                    <ul className="space-y-3">
                                        {plan.features.map((feature) => (
                                            <li key={feature} className="flex items-start gap-2">
                                                <Check className="w-5 h-5 text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
                                                <span className="text-gray-700 dark:text-gray-300">{feature}</span>
                                            </li>
                                        ))}
                                    </ul>
                                </CardContent>
                                <CardFooter>
                                    <Button
                                        className="w-full"
                                        variant={plan.id === currentPlan ? 'outline' : plan.highlighted ? 'default' : 'outline'}
                                        size="lg"
                                        onClick={() => handleUpgrade(plan.id)}
                                        disabled={isButtonDisabled(plan)}
                                    >
                                        {loading === plan.id ? (
                                            <>
                                                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                                                Processing...
                                            </>
                                        ) : (
                                            getButtonText(plan)
                                        )}
                                    </Button>
                                </CardFooter>
                            </Card>
                        </motion.div>
                    ))}
                </div>
            </div>
        </div>
    );
}
