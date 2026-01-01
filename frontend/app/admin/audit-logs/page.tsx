'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { adminAPI } from '@/lib/api';
import { useAuthStore } from '@/lib/store';

interface AuditLog {
    id: string;
    user_id: string;
    action: string;
    resource_type: string | null;
    resource_id: string | null;
    timestamp: string;
    metadata: any;
}

export default function AuditLogsPage() {
    const router = useRouter();
    const { user, isAuthenticated } = useAuthStore();
    const [logs, setLogs] = useState<AuditLog[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!isAuthenticated || (user?.role !== 'college_admin' && user?.role !== 'platform_admin')) {
            router.push('/dashboard');
            return;
        }

        loadLogs();
    }, [isAuthenticated, user, router]);

    const loadLogs = async () => {
        try {
            const response = await adminAPI.getAuditLogs(100);
            setLogs(response.data);
        } catch (error) {
            console.error('Failed to load logs:', error);
        } finally {
            setLoading(false);
        }
    };

    const getActionColor = (action: string) => {
        if (action.includes('login')) return 'text-green-600 bg-green-100 dark:bg-green-900/30';
        if (action.includes('generate')) return 'text-blue-600 bg-blue-100 dark:bg-blue-900/30';
        if (action.includes('download')) return 'text-purple-600 bg-purple-100 dark:bg-purple-900/30';
        return 'text-gray-600 bg-gray-100 dark:bg-gray-700/30';
    };

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="flex items-center justify-between">
                        <h1 className="text-2xl font-bold">Audit Logs</h1>
                        <Button variant="outline" onClick={() => router.push('/admin')}>
                            Back to Admin
                        </Button>
                    </div>
                </div>
            </header>

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <Card>
                    <CardHeader>
                        <CardTitle>Activity Trail</CardTitle>
                    </CardHeader>
                    <CardContent>
                        {loading ? (
                            <div className="text-center py-8">Loading...</div>
                        ) : logs.length === 0 ? (
                            <div className="text-center py-8 text-gray-500">No audit logs found</div>
                        ) : (
                            <div className="space-y-3">
                                {logs.map((log) => (
                                    <div
                                        key={log.id}
                                        className="flex items-start justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800"
                                    >
                                        <div className="flex-1">
                                            <div className="flex items-center gap-2 mb-1">
                                                <span className={`px-2 py-1 rounded text-xs font-medium ${getActionColor(log.action)}`}>
                                                    {log.action}
                                                </span>
                                                {log.resource_type && (
                                                    <span className="text-xs text-gray-500">
                                                        {log.resource_type}
                                                    </span>
                                                )}
                                            </div>
                                            <p className="text-sm text-gray-600 dark:text-gray-400">
                                                User: {log.user_id?.slice(0, 8)}...
                                            </p>
                                            {log.metadata && Object.keys(log.metadata).length > 0 && (
                                                <p className="text-xs text-gray-500 mt-1">
                                                    {JSON.stringify(log.metadata).slice(0, 100)}...
                                                </p>
                                            )}
                                        </div>
                                        <div className="text-right text-sm text-gray-500">
                                            {new Date(log.timestamp).toLocaleString()}
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
