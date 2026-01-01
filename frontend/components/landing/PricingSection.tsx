'use client';

import { motion } from 'framer-motion';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Check } from 'lucide-react';
import { useRouter } from 'next/navigation';

const pricingPlans = [
    {
        id: 'free',
        name: 'Free',
        price: '₹0',
        period: '/month',
        description: 'Perfect for trying out ProjectGen',
        features: [
            '2 projects per month',
            'All document types (DOCX, PPTX)',
            'Basic plagiarism check',
            'Email support',
        ],
        cta: 'Get Started',
        highlighted: false,
    },
    {
        id: 'pro',
        name: 'Pro',
        price: '₹299',
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
        price: 'Custom',
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

export default function PricingSection() {
    const router = useRouter();

    const handleClick = (planId: string) => {
        if (planId === 'enterprise') {
            window.open('mailto:support@projectgen.ai?subject=Enterprise Plan Inquiry', '_blank');
        } else {
            // All plans redirect to register - users can upgrade after login
            router.push('/auth/register');
        }
    };

    return (
        <section id="pricing" className="py-20 bg-gradient-to-br from-purple-50 via-white to-blue-50 dark:from-gray-900 dark:via-purple-900/10 dark:to-gray-900">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.8 }}
                    className="text-center mb-16"
                >
                    <h2 className="text-4xl md:text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-purple-600 to-blue-600 dark:from-purple-400 dark:to-blue-400">
                        Simple, Transparent Pricing
                    </h2>
                    <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
                        Choose the plan that fits your needs. No hidden fees.
                    </p>
                </motion.div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {pricingPlans.map((plan, index) => (
                        <motion.div
                            key={plan.name}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.5, delay: index * 0.1 }}
                            className={plan.highlighted ? 'md:-mt-4' : ''}
                        >
                            <Card className={`h-full flex flex-col ${plan.highlighted
                                ? 'border-purple-500 dark:border-purple-400 shadow-xl scale-105'
                                : 'border-gray-200 dark:border-gray-700'
                                }`}>
                                {plan.highlighted && (
                                    <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white text-center py-2 rounded-t-lg font-semibold">
                                        Most Popular
                                    </div>
                                )}
                                <CardHeader>
                                    <CardTitle className="text-2xl">{plan.name}</CardTitle>
                                    <CardDescription>{plan.description}</CardDescription>
                                    <div className="mt-4">
                                        <span className="text-4xl font-bold">{plan.price}</span>
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
                                        variant={plan.highlighted ? 'default' : 'outline'}
                                        size="lg"
                                        onClick={() => handleClick(plan.id)}
                                    >
                                        {plan.cta}
                                    </Button>
                                </CardFooter>
                            </Card>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}
