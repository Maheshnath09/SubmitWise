'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { useAuthStore } from '@/lib/store';
import { projectsAPI, paymentsAPI } from '@/lib/api';
import { Sparkles, FileText, Clock, Download, Crown, Zap } from 'lucide-react';

interface Project {
    id: string;
    job_id: string;
    title: string | null;
    subject: string | null;
    status: string;
    created_at: string;
    completed_at: string | null;
}

interface Subscription {
    subscription_tier: string;
    credits: number;
    plan_name: string;
}

export default function DashboardPage() {
    const router = useRouter();
    const { user, isAuthenticated, logout, hasHydrated } = useAuthStore();
    const [projects, setProjects] = useState<Project[]>([]);
    const [loading, setLoading] = useState(true);
    const [subscription, setSubscription] = useState<Subscription>({
        subscription_tier: 'free',
        credits: 2,
        plan_name: 'Free'
    });

    useEffect(() => {
        // Wait for hydration before checking auth
        if (!hasHydrated) return;

        if (!isAuthenticated) {
            router.push('/auth/login');
            return;
        }

        loadProjects();
        loadSubscription();
    }, [isAuthenticated, hasHydrated, router]);

    const loadProjects = async () => {
        try {
            const response = await projectsAPI.getHistory();
            setProjects(response.data);
        } catch (error) {
            console.error('Failed to load projects:', error);
        } finally {
            setLoading(false);
        }
    };

    const loadSubscription = async () => {
        try {
            const response = await paymentsAPI.getSubscription();
            setSubscription({
                subscription_tier: response.data.subscription_tier || 'free',
                credits: response.data.credits || 2,
                plan_name: response.data.plan_name || 'Free'
            });
        } catch (error) {
            console.error('Failed to load subscription:', error);
        }
    };

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'completed': return 'text-green-600 bg-green-100 dark:bg-green-900/30';
            case 'processing': return 'text-blue-600 bg-blue-100 dark:bg-blue-900/30';
            case 'failed': return 'text-red-600 bg-red-100 dark:bg-red-900/30';
            default: return 'text-gray-600 bg-gray-100 dark:bg-gray-700/30';
        }
    };

    const getPlanBadgeColor = (tier: string) => {
        switch (tier) {
            case 'pro': return 'bg-gradient-to-r from-purple-500 to-blue-500 text-white';
            case 'enterprise': return 'bg-gradient-to-r from-yellow-500 to-orange-500 text-white';
            default: return 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300';
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            {/* Header */}
            <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-2xl font-bold">ProjectGen</h1>
                            <p className="text-sm text-gray-600 dark:text-gray-400">Welcome back, {user?.email}</p>
                        </div>
                        <div className="flex items-center gap-4">
                            {/* Plan Badge */}
                            <div className={`px-3 py-1 rounded-full text-sm font-semibold ${getPlanBadgeColor(subscription.subscription_tier)}`}>
                                <Crown className="w-3 h-3 inline mr-1" />
                                {subscription.plan_name}
                            </div>
                            {/* Upgrade or Manage Plan */}
                            {subscription.subscription_tier === 'free' ? (
                                <Link href="/pricing">
                                    <Button variant="default" className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700">
                                        <Zap className="w-4 h-4 mr-2" />
                                        Upgrade
                                    </Button>
                                </Link>
                            ) : (
                                <Link href="/pricing">
                                    <Button variant="outline">
                                        <Crown className="w-4 h-4 mr-2" />
                                        Manage Plan
                                    </Button>
                                </Link>
                            )}
                            <Button variant="outline" onClick={logout}>
                                Logout
                            </Button>
                        </div>
                    </div>
                </div>
            </header>

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Quick Actions */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    <Card className="hover:shadow-lg transition-shadow cursor-pointer" onClick={() => router.push('/generate')}>
                        <CardHeader>
                            <Sparkles className="w-8 h-8 text-purple-600 mb-2" />
                            <CardTitle>Generate New Project</CardTitle>
                            <CardDescription>Create a new AI-powered project</CardDescription>
                        </CardHeader>
                    </Card>

                    <Card>
                        <CardHeader>
                            <FileText className="w-8 h-8 text-blue-600 mb-2" />
                            <CardTitle>{projects.length}</CardTitle>
                            <CardDescription>Total Projects</CardDescription>
                        </CardHeader>
                    </Card>

                    <Card>
                        <CardHeader>
                            <Clock className="w-8 h-8 text-green-600 mb-2" />
                            <CardTitle>{projects.filter(p => p.status === 'completed').length}</CardTitle>
                            <CardDescription>Completed Projects</CardDescription>
                        </CardHeader>
                    </Card>

                    {subscription.subscription_tier === 'free' ? (
                        <Card className="hover:shadow-lg transition-shadow cursor-pointer bg-gradient-to-br from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 border-purple-200 dark:border-purple-700" onClick={() => router.push('/pricing')}>
                            <CardHeader>
                                <Crown className="w-8 h-8 text-yellow-500 mb-2" />
                                <CardTitle>Upgrade Plan</CardTitle>
                                <CardDescription>Get more credits & premium features</CardDescription>
                            </CardHeader>
                        </Card>
                    ) : (
                        <Card className="bg-gradient-to-br from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 border-purple-200 dark:border-purple-700">
                            <CardHeader>
                                <Zap className="w-8 h-8 text-yellow-500 mb-2" />
                                <CardTitle className="text-3xl font-bold text-purple-600 dark:text-purple-400">{subscription.credits}</CardTitle>
                                <CardDescription>Available Credits</CardDescription>
                            </CardHeader>
                        </Card>
                    )}
                </div>

                {/* Recent Projects */}
                <Card>
                    <CardHeader>
                        <CardTitle>Recent Projects</CardTitle>
                        <CardDescription>Your project generation history</CardDescription>
                    </CardHeader>
                    <CardContent>
                        {loading ? (
                            <div className="text-center py-8 text-gray-500">Loading...</div>
                        ) : projects.length === 0 ? (
                            <div className="text-center py-8">
                                <p className="text-gray-500 mb-4">No projects yet</p>
                                <Link href="/generate">
                                    <Button>
                                        <Sparkles className="w-4 h-4 mr-2" />
                                        Generate Your First Project
                                    </Button>
                                </Link>
                            </div>
                        ) : (
                            <div className="space-y-4">
                                {projects.map((project) => (
                                    <div
                                        key={project.id}
                                        className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                                    >
                                        <div className="flex-1">
                                            <h3 className="font-semibold">{project.title || 'Untitled Project'}</h3>
                                            <p className="text-sm text-gray-600 dark:text-gray-400">
                                                {project.subject} • {new Date(project.created_at).toLocaleDateString()}
                                            </p>
                                        </div>
                                        <div className="flex items-center gap-4">
                                            <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(project.status)}`}>
                                                {project.status}
                                            </span>
                                            {project.status === 'completed' && (
                                                <Link href={`/projects/${project.job_id}`}>
                                                    <Button size="sm">
                                                        <Download className="w-4 h-4 mr-2" />
                                                        View
                                                    </Button>
                                                </Link>
                                            )}
                                            {project.status === 'processing' && (
                                                <Link href={`/projects/${project.job_id}`}>
                                                    <Button size="sm" variant="outline">
                                                        View Status
                                                    </Button>
                                                </Link>
                                            )}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </CardContent>
                </Card>
            </main>
        </div>
    );
}
