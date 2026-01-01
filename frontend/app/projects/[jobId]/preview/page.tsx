'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { projectsAPI } from '@/lib/api';
import { Loader2, Download } from 'lucide-react';

interface ProjectPreview {
    job_id: string;
    title: string;
    abstract: string;
    keywords: string[];
    modules: any[];
    difficulty: string;
    timeline_days: number;
}

export default function ProjectPreviewPage({ params }: { params: { jobId: string } }) {
    const router = useRouter();
    const [preview, setPreview] = useState<ProjectPreview | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadPreview();
    }, [params.jobId]);

    const loadPreview = async () => {
        try {
            const response = await projectsAPI.getPreview(params.jobId);
            setPreview(response.data);
        } catch (error) {
            console.error('Failed to load preview:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <Loader2 className="w-8 h-8 animate-spin" />
            </div>
        );
    }

    if (!preview) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <p>Preview not available</p>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
                    <Button variant="outline" onClick={() => router.push(`/projects/${params.jobId}`)}>
                        ← Back
                    </Button>
                    <Button onClick={() => router.push(`/projects/${params.jobId}`)}>
                        <Download className="w-4 h-4 mr-2" />
                        Download
                    </Button>
                </div>
            </header>

            <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
                {/* Title */}
                <Card>
                    <CardHeader>
                        <CardTitle className="text-3xl">{preview.title}</CardTitle>
                        <div className="flex gap-2 mt-2">
                            <span className="px-3 py-1 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 rounded-full text-sm">
                                {preview.difficulty}
                            </span>
                            <span className="px-3 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded-full text-sm">
                                {preview.timeline_days} days
                            </span>
                        </div>
                    </CardHeader>
                </Card>

                {/* Abstract */}
                <Card>
                    <CardHeader>
                        <CardTitle>Abstract</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-gray-700 dark:text-gray-300">{preview.abstract}</p>
                    </CardContent>
                </Card>

                {/* Keywords */}
                <Card>
                    <CardHeader>
                        <CardTitle>Keywords</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="flex flex-wrap gap-2">
                            {preview.keywords.map((keyword, idx) => (
                                <span
                                    key={idx}
                                    className="px-3 py-1 bg-gray-100 dark:bg-gray-800 rounded-full text-sm"
                                >
                                    {keyword}
                                </span>
                            ))}
                        </div>
                    </CardContent>
                </Card>

                {/* Modules */}
                <Card>
                    <CardHeader>
                        <CardTitle>Project Modules</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        {preview.modules.map((module, idx) => (
                            <div key={idx} className="border-l-4 border-primary pl-4">
                                <h3 className="font-semibold text-lg">{module.name}</h3>
                                <p className="text-gray-600 dark:text-gray-400 mt-1">{module.description}</p>
                                <p className="text-sm text-gray-500 mt-2">Duration: {module.weeks} weeks</p>
                                {module.dependencies && module.dependencies.length > 0 && (
                                    <p className="text-sm text-gray-500">
                                        Dependencies: {module.dependencies.join(', ')}
                                    </p>
                                )}
                            </div>
                        ))}
                    </CardContent>
                </Card>
            </main>
        </div>
    );
}
