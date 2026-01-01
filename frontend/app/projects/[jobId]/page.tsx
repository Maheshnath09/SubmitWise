'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { projectsAPI } from '@/lib/api';
import { Loader2, CheckCircle, XCircle, Download, Eye, AlertTriangle } from 'lucide-react';

interface ProjectStatus {
    job_id: string;
    status: string;
    title: string | null;
    error_message: string | null;
    created_at: string;
    completed_at: string | null;
    plagiarism_score: number | null;
    plagiarism_warnings: any;
}

export default function ProjectStatusPage({ params }: { params: { jobId: string } }) {
    const router = useRouter();
    const [status, setStatus] = useState<ProjectStatus | null>(null);
    const [loading, setLoading] = useState(true);
    const [downloadUrl, setDownloadUrl] = useState<string | null>(null);

    useEffect(() => {
        pollStatus();
        const interval = setInterval(pollStatus, 2000); // Poll every 2 seconds

        return () => clearInterval(interval);
    }, [params.jobId]);

    const pollStatus = async () => {
        try {
            const response = await projectsAPI.getStatus(params.jobId);
            setStatus(response.data);
            setLoading(false);

            // If completed, get download URL
            if (response.data.status === 'completed' && !downloadUrl) {
                const downloadResponse = await projectsAPI.getDownload(params.jobId);
                setDownloadUrl(downloadResponse.data.zip_url);
            }
        } catch (error) {
            console.error('Failed to fetch status:', error);
            setLoading(false);
        }
    };

    const getProgress = () => {
        if (!status) return 0;
        switch (status.status) {
            case 'pending': return 10;
            case 'processing': return 50;
            case 'completed': return 100;
            case 'failed': return 0;
            default: return 0;
        }
    };

    const getStatusIcon = () => {
        if (!status) return <Loader2 className="w-12 h-12 animate-spin text-blue-600" />;

        switch (status.status) {
            case 'pending':
            case 'processing':
                return <Loader2 className="w-12 h-12 animate-spin text-blue-600" />;
            case 'completed':
                return <CheckCircle className="w-12 h-12 text-green-600" />;
            case 'failed':
                return <XCircle className="w-12 h-12 text-red-600" />;
            default:
                return <Loader2 className="w-12 h-12 animate-spin text-blue-600" />;
        }
    };

    const getStatusMessage = () => {
        if (!status) return 'Loading...';

        switch (status.status) {
            case 'pending':
                return 'Your project is in queue...';
            case 'processing':
                return 'AI is generating your project...';
            case 'completed':
                return 'Project generated successfully!';
            case 'failed':
                return 'Project generation failed';
            default:
                return 'Processing...';
        }
    };

    if (loading && !status) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <Loader2 className="w-8 h-8 animate-spin" />
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <Button variant="outline" onClick={() => router.push('/dashboard')}>
                        ← Back to Dashboard
                    </Button>
                </div>
            </header>

            <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <Card>
                    <CardHeader className="text-center">
                        <div className="flex justify-center mb-4">
                            {getStatusIcon()}
                        </div>
                        <CardTitle className="text-2xl">{getStatusMessage()}</CardTitle>
                        <CardDescription>
                            {status?.title || 'Project Generation'}
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        {/* Progress Bar */}
                        {status?.status !== 'failed' && (
                            <div className="space-y-2">
                                <Progress value={getProgress()} />
                                <p className="text-sm text-center text-gray-600 dark:text-gray-400">
                                    {getProgress()}% Complete
                                </p>
                            </div>
                        )}

                        {/* Error Message */}
                        {status?.status === 'failed' && status.error_message && (
                            <div className="bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 p-4 rounded-md">
                                <p className="font-semibold mb-1">Error:</p>
                                <p>{status.error_message}</p>
                            </div>
                        )}

                        {/* Plagiarism Warning */}
                        {status?.status === 'completed' && status.plagiarism_score && status.plagiarism_score > 0.8 && (
                            <div className="bg-yellow-50 dark:bg-yellow-900/20 text-yellow-800 dark:text-yellow-200 p-4 rounded-md flex items-start gap-2">
                                <AlertTriangle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                                <div>
                                    <p className="font-semibold">Plagiarism Warning</p>
                                    <p className="text-sm">
                                        Similarity score: {(status.plagiarism_score * 100).toFixed(1)}%
                                    </p>
                                    {status.plagiarism_warnings?.warnings?.map((warning: string, idx: number) => (
                                        <p key={idx} className="text-sm mt-1">• {warning}</p>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Actions */}
                        {status?.status === 'completed' && (
                            <div className="flex gap-4">
                                <Button
                                    className="flex-1"
                                    onClick={() => router.push(`/projects/${params.jobId}/preview`)}
                                >
                                    <Eye className="w-4 h-4 mr-2" />
                                    Preview
                                </Button>
                                {downloadUrl && (
                                    <Button
                                        className="flex-1"
                                        variant="default"
                                        onClick={async () => {
                                            try {
                                                // Create filename from project title
                                                const title = status?.title || 'Project';
                                                const safeTitle = title.replace(/[^a-zA-Z0-9 -]/g, '').replace(/\s+/g, '_');
                                                const filename = `${safeTitle}_project.zip`;

                                                // Get the auth token
                                                const token = localStorage.getItem('access_token');
                                                const fullUrl = token
                                                    ? `${downloadUrl}${downloadUrl.includes('?') ? '&' : '?'}token=${token}`
                                                    : downloadUrl;

                                                // Fetch the file
                                                const response = await fetch(fullUrl);
                                                if (!response.ok) {
                                                    throw new Error(`Download failed: ${response.status}`);
                                                }

                                                // Get the raw data and create a properly typed blob
                                                const arrayBuffer = await response.arrayBuffer();
                                                const blob = new Blob([arrayBuffer], { type: 'application/zip' });

                                                // FileSaver-style download
                                                // Check for IE/Edge legacy
                                                if ((navigator as any).msSaveBlob) {
                                                    (navigator as any).msSaveBlob(blob, filename);
                                                    return;
                                                }

                                                // For modern browsers - create object URL
                                                const blobUrl = URL.createObjectURL(blob);

                                                // Create and style the link
                                                const link = document.createElement('a');
                                                link.href = blobUrl;
                                                link.download = filename;
                                                link.style.position = 'fixed';
                                                link.style.left = '-9999px';
                                                link.style.top = '-9999px';

                                                // Append, click, remove
                                                document.body.appendChild(link);
                                                link.click();
                                                document.body.removeChild(link);

                                                // Delay cleanup to ensure download starts
                                                setTimeout(() => URL.revokeObjectURL(blobUrl), 1000);

                                            } catch (error) {
                                                console.error('Download failed:', error);
                                                alert('Download failed: ' + (error as Error).message);
                                            }
                                        }}
                                    >
                                        <Download className="w-4 h-4 mr-2" />
                                        Download ZIP
                                    </Button>
                                )}
                            </div>
                        )}

                        {/* Status Details */}
                        <div className="border-t border-gray-200 dark:border-gray-700 pt-4 space-y-2 text-sm">
                            <div className="flex justify-between">
                                <span className="text-gray-600 dark:text-gray-400">Job ID:</span>
                                <span className="font-mono">{params.jobId.slice(0, 8)}...</span>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-gray-600 dark:text-gray-400">Created:</span>
                                <span>{status?.created_at ? new Date(status.created_at).toLocaleString() : '-'}</span>
                            </div>
                            {status?.completed_at && (
                                <div className="flex justify-between">
                                    <span className="text-gray-600 dark:text-gray-400">Completed:</span>
                                    <span>{new Date(status.completed_at).toLocaleString()}</span>
                                </div>
                            )}
                        </div>
                    </CardContent>
                </Card>
            </main>
        </div>
    );
}
