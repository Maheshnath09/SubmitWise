'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { adminAPI } from '@/lib/api';
import { useAuthStore } from '@/lib/store';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Users, FileText, TrendingUp, Activity } from 'lucide-react';

interface UsageStats {
    total_users: number;
    total_projects: number;
    completed_projects: number;
    projects_by_status: Record<string, number>;
    recent_projects_30d: number;
    projects_by_difficulty: Record<string, number>;
}

const COLORS = ['#8B5CF6', '#3B82F6', '#10B981', '#F59E0B', '#EF4444'];

export default function AdminDashboard() {
    const router = useRouter();
    const { user, isAuthenticated, hasHydrated } = useAuthStore();
    const [stats, setStats] = useState<UsageStats | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        console.log('Admin Page Auth State:', { isAuthenticated, role: user?.role, user });
        if (hasHydrated && (!isAuthenticated || (user?.role !== 'college_admin' && user?.role !== 'platform_admin'))) {
            console.log('Redirecting to dashboard. Reason:', !isAuthenticated ? 'Not authenticated' : `Invalid role: ${user?.role}`);
            router.push('/dashboard');
            return;
        }

        if (isAuthenticated) {
            loadStats();
        }
    }, [isAuthenticated, user, router, hasHydrated]);

    const loadStats = async () => {
        try {
            const response = await adminAPI.getUsageStats();
            setStats(response.data);
        } catch (error) {
            console.error('Failed to load stats:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
    }

    if (!stats) {
        return <div className="min-h-screen flex items-center justify-center">Failed to load stats</div>;
    }

    // Prepare chart data
    const statusData = Object.entries(stats.projects_by_status).map(([name, value]) => ({
        name: name.charAt(0).toUpperCase() + name.slice(1),
        value
    }));

    const difficultyData = Object.entries(stats.projects_by_difficulty).map(([name, value]) => ({
        name,
        value
    }));

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            {/* Header */}
            <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-2xl font-bold">Admin Dashboard</h1>
                            <p className="text-sm text-gray-600 dark:text-gray-400">
                                {user?.role === 'platform_admin' ? 'Platform' : 'College'} Analytics
                            </p>
                        </div>
                        <Button variant="outline" onClick={() => router.push('/dashboard')}>
                            Back to Dashboard
                        </Button>
                    </div>
                </div>
            </header>

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Stats Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between pb-2">
                            <CardTitle className="text-sm font-medium text-gray-600 dark:text-gray-400">
                                Total Users
                            </CardTitle>
                            <Users className="w-4 h-4 text-purple-600" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-3xl font-bold">{stats.total_users}</div>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between pb-2">
                            <CardTitle className="text-sm font-medium text-gray-600 dark:text-gray-400">
                                Total Projects
                            </CardTitle>
                            <FileText className="w-4 h-4 text-blue-600" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-3xl font-bold">{stats.total_projects}</div>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between pb-2">
                            <CardTitle className="text-sm font-medium text-gray-600 dark:text-gray-400">
                                Completed
                            </CardTitle>
                            <TrendingUp className="w-4 h-4 text-green-600" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-3xl font-bold">{stats.completed_projects}</div>
                            <p className="text-xs text-gray-500 mt-1">
                                {stats.total_projects > 0
                                    ? `${((stats.completed_projects / stats.total_projects) * 100).toFixed(1)}% success rate`
                                    : 'No projects yet'}
                            </p>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between pb-2">
                            <CardTitle className="text-sm font-medium text-gray-600 dark:text-gray-400">
                                Last 30 Days
                            </CardTitle>
                            <Activity className="w-4 h-4 text-orange-600" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-3xl font-bold">{stats.recent_projects_30d}</div>
                        </CardContent>
                    </Card>
                </div>

                {/* Charts */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                    {/* Projects by Status */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Projects by Status</CardTitle>
                            <CardDescription>Distribution of project statuses</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <ResponsiveContainer width="100%" height={300}>
                                <PieChart>
                                    <Pie
                                        data={statusData}
                                        cx="50%"
                                        cy="50%"
                                        labelLine={false}
                                        label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                                        outerRadius={80}
                                        fill="#8884d8"
                                        dataKey="value"
                                    >
                                        {statusData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                        ))}
                                    </Pie>
                                    <Tooltip />
                                </PieChart>
                            </ResponsiveContainer>
                        </CardContent>
                    </Card>

                    {/* Projects by Difficulty */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Projects by Difficulty</CardTitle>
                            <CardDescription>Distribution across difficulty levels</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <ResponsiveContainer width="100%" height={300}>
                                <BarChart data={difficultyData}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="name" />
                                    <YAxis />
                                    <Tooltip />
                                    <Legend />
                                    <Bar dataKey="value" fill="#8B5CF6" />
                                </BarChart>
                            </ResponsiveContainer>
                        </CardContent>
                    </Card>
                </div>

                {/* Quick Actions */}
                <Card>
                    <CardHeader>
                        <CardTitle>Quick Actions</CardTitle>
                        <CardDescription>Administrative tools and features</CardDescription>
                    </CardHeader>
                    <CardContent className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <Button variant="outline" className="h-20" disabled>
                            <div className="text-center">
                                <p className="font-semibold">Bulk Upload</p>
                                <p className="text-xs text-gray-500">CSV student onboarding</p>
                            </div>
                        </Button>
                        <Button variant="outline" className="h-20" onClick={() => router.push('/admin/audit-logs')}>
                            <div className="text-center">
                                <p className="font-semibold">Audit Logs</p>
                                <p className="text-xs text-gray-500">View activity trail</p>
                            </div>
                        </Button>
                        <Button variant="outline" className="h-20" disabled>
                            <div className="text-center">
                                <p className="font-semibold">Templates</p>
                                <p className="text-xs text-gray-500">Manage custom templates</p>
                            </div>
                        </Button>
                    </CardContent>
                </Card>
            </main>
        </div>
    );
}
