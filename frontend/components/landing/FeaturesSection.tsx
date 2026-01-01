'use client';

import { motion } from 'framer-motion';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Brain, Zap, FileCheck, Shield, Globe, Clock } from 'lucide-react';

const features = [
    {
        icon: Brain,
        title: 'AI-Powered Generation',
        description: 'Advanced Groq GPT-OSS-120B model generates contextually relevant projects tailored to Indian curriculum.',
        color: 'text-purple-600 dark:text-purple-400',
        bgColor: 'bg-purple-100 dark:bg-purple-900/30',
    },
    {
        icon: Zap,
        title: 'Lightning Fast',
        description: 'Get your complete project bundle in minutes, not days. Perfect for tight deadlines.',
        color: 'text-yellow-600 dark:text-yellow-400',
        bgColor: 'bg-yellow-100 dark:bg-yellow-900/30',
    },
    {
        icon: FileCheck,
        title: 'Complete Deliverables',
        description: 'Code, DOCX report, PPTX slides, viva questions, and marking rubric - everything you need.',
        color: 'text-blue-600 dark:text-blue-400',
        bgColor: 'bg-blue-100 dark:bg-blue-900/30',
    },
    {
        icon: Shield,
        title: 'Plagiarism Check',
        description: 'Built-in plagiarism detection ensures your project is unique and original.',
        color: 'text-green-600 dark:text-green-400',
        bgColor: 'bg-green-100 dark:bg-green-900/30',
    },
    {
        icon: Globe,
        title: 'Multi-Language Support',
        description: 'Generate projects in English or Hindi to match your preference.',
        color: 'text-pink-600 dark:text-pink-400',
        bgColor: 'bg-pink-100 dark:bg-pink-900/30',
    },
    {
        icon: Clock,
        title: 'Semester Planning',
        description: 'Detailed module breakdown with timeline and dependencies for smooth execution.',
        color: 'text-indigo-600 dark:text-indigo-400',
        bgColor: 'bg-indigo-100 dark:bg-indigo-900/30',
    },
];

export default function FeaturesSection() {
    return (
        <section id="features" className="py-20 bg-white dark:bg-gray-900">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.8 }}
                    className="text-center mb-16"
                >
                    <h2 className="text-4xl md:text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-purple-600 to-blue-600 dark:from-purple-400 dark:to-blue-400">
                        Everything You Need for Success
                    </h2>
                    <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
                        Powerful features designed specifically for Indian college students
                    </p>
                </motion.div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {features.map((feature, index) => (
                        <motion.div
                            key={feature.title}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.5, delay: index * 0.1 }}
                        >
                            <Card className="h-full hover:shadow-lg transition-shadow duration-300 border-2 hover:border-purple-200 dark:hover:border-purple-800">
                                <CardHeader>
                                    <div className={`w-12 h-12 rounded-lg ${feature.bgColor} flex items-center justify-center mb-4`}>
                                        <feature.icon className={`w-6 h-6 ${feature.color}`} />
                                    </div>
                                    <CardTitle className="text-xl">{feature.title}</CardTitle>
                                    <CardDescription className="text-base">
                                        {feature.description}
                                    </CardDescription>
                                </CardHeader>
                            </Card>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}
