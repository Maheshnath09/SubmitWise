'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { projectsAPI } from '@/lib/api';
import { useAuthStore } from '@/lib/store';
import { Loader2, Sparkles, AlertCircle } from 'lucide-react';

export default function GeneratePage() {
    const router = useRouter();
    const { user, isAuthenticated, hasHydrated } = useAuthStore();

    const [formData, setFormData] = useState({
        subject: '',
        semester: user?.semester?.toString() || '',
        difficulty: 'Intermediate',
        additional_requirements: '',
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        // Wait for hydration before checking auth
        if (!hasHydrated) return;

        if (!isAuthenticated) {
            router.push('/auth/login');
        }
    }, [isAuthenticated, hasHydrated, router]);

    // Show loading while hydrating or not authenticated
    if (!hasHydrated || !isAuthenticated) {
        return (
            <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
                <div className="text-center">
                    <Loader2 className="w-8 h-8 animate-spin mx-auto text-purple-600" />
                    <p className="mt-2 text-gray-600 dark:text-gray-400">Loading...</p>
                </div>
            </div>
        );
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        if ((user?.credits || 0) <= 0) {
            setError('Insufficient credits. Please purchase more credits to continue.');
            return;
        }

        setLoading(true);

        try {
            const response = await projectsAPI.generate({
                subject: formData.subject,
                semester: parseInt(formData.semester),
                difficulty: formData.difficulty,
                additional_requirements: formData.additional_requirements,
            });

            router.push(`/projects/${response.data.job_id}`);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to start project generation. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            {/* Header */}
            <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="flex items-center justify-between">
                        <h1 className="text-2xl font-bold">Generate Project</h1>
                        <div className="flex items-center gap-4">
                            <Button variant="outline" onClick={() => router.push('/dashboard')}>
                                Back to Dashboard
                            </Button>
                        </div>
                    </div>
                </div>
            </header>

            <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Sparkles className="w-6 h-6 text-purple-600" />
                            Create Your Project
                        </CardTitle>
                        <CardDescription>
                            Fill in the details below to generate a complete semester project with AI
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <form onSubmit={handleSubmit} className="space-y-6">
                            <div className="space-y-2">
                                <Label htmlFor="subject">Subject / Topic *</Label>
                                <Input
                                    id="subject"
                                    placeholder="e.g., Computer Networks, Web Development, Machine Learning"
                                    value={formData.subject}
                                    onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                                    required
                                />
                                <p className="text-sm text-gray-500">Enter the subject or topic for your project</p>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label htmlFor="semester">Semester *</Label>
                                    <Input
                                        id="semester"
                                        type="number"
                                        min="1"
                                        max="8"
                                        placeholder="5"
                                        value={formData.semester}
                                        onChange={(e) => setFormData({ ...formData, semester: e.target.value })}
                                        required
                                    />
                                </div>

                                <div className="space-y-2">
                                    <Label htmlFor="difficulty">Difficulty Level *</Label>
                                    <Select
                                        id="difficulty"
                                        value={formData.difficulty}
                                        onChange={(e) => setFormData({ ...formData, difficulty: e.target.value })}
                                        required
                                    >
                                        <option value="Beginner">Beginner</option>
                                        <option value="Intermediate">Intermediate</option>
                                        <option value="Advanced">Advanced</option>
                                    </Select>
                                </div>
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="requirements">Additional Requirements (Optional)</Label>
                                <Textarea
                                    id="requirements"
                                    placeholder="e.g., Include authentication, Use React for frontend, Focus on security aspects..."
                                    value={formData.additional_requirements}
                                    onChange={(e) => setFormData({ ...formData, additional_requirements: e.target.value })}
                                    rows={4}
                                />
                                <p className="text-sm text-gray-500">
                                    Specify any additional requirements or preferences for your project
                                </p>
                            </div>

                            {error && (
                                <div className="bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 p-4 rounded-md flex items-start gap-2">
                                    <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                                    <span>{error}</span>
                                </div>
                            )}

                            <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-md">
                                <h4 className="font-semibold text-blue-900 dark:text-blue-100 mb-2">What you'll get:</h4>
                                <ul className="space-y-1 text-sm text-blue-800 dark:text-blue-200">
                                    <li>✓ Complete project abstract and modules</li>
                                    <li>✓ Starter code with proper structure</li>
                                    <li>✓ Professional DOCX report</li>
                                    <li>✓ PPTX presentation slides</li>
                                    <li>✓ Viva questions and answers</li>
                                    <li>✓ Marking rubric</li>
                                    <li>✓ Everything in a downloadable ZIP</li>
                                </ul>
                            </div>

                            <Button type="submit" className="w-full" size="lg" disabled={loading || (user?.credits || 0) <= 0}>
                                {loading && <Loader2 className="mr-2 h-5 w-5 animate-spin" />}
                                {!loading && <Sparkles className="mr-2 h-5 w-5" />}
                                Generate Project (1 Credit)
                            </Button>
                        </form>
                    </CardContent>
                </Card>
            </main>
        </div>
    );
}
