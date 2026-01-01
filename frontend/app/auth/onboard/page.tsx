'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { authAPI } from '@/lib/api';
import { useAuthStore } from '@/lib/store';
import { Loader2, CheckCircle } from 'lucide-react';

export default function OnboardPage() {
    const router = useRouter();
    const updateUser = useAuthStore((state) => state.updateUser);

    const [step, setStep] = useState(1);
    const [formData, setFormData] = useState({
        college_name: '',
        semester: '',
        subjects: '',
        language: 'english',
    });
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);

        try {
            await authAPI.onboard({
                college_name: formData.college_name,
                semester: parseInt(formData.semester),
                subjects: formData.subjects.split(',').map(s => s.trim()),
                language: formData.language,
            });

            updateUser({
                semester: parseInt(formData.semester),
                subjects: formData.subjects.split(',').map(s => s.trim()),
                language: formData.language,
            });

            router.push('/dashboard');
        } catch (err) {
            console.error('Onboarding failed:', err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 via-white to-blue-50 dark:from-gray-900 dark:via-purple-900/20 dark:to-gray-900 p-4">
            <Card className="w-full max-w-2xl">
                <CardHeader>
                    <CardTitle className="text-2xl">Complete Your Profile</CardTitle>
                    <CardDescription>
                        Help us personalize your experience
                    </CardDescription>

                    {/* Progress indicator */}
                    <div className="flex items-center gap-2 mt-4">
                        {[1, 2, 3].map((s) => (
                            <div key={s} className="flex items-center gap-2 flex-1">
                                <div className={`h-2 flex-1 rounded-full ${s <= step ? 'bg-primary' : 'bg-gray-200 dark:bg-gray-700'}`} />
                            </div>
                        ))}
                    </div>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-6">
                        {step === 1 && (
                            <div className="space-y-4">
                                <h3 className="font-semibold text-lg">College Information</h3>
                                <div className="space-y-2">
                                    <Label htmlFor="college">College Name</Label>
                                    <Input
                                        id="college"
                                        placeholder="e.g., ABC Engineering College"
                                        value={formData.college_name}
                                        onChange={(e) => setFormData({ ...formData, college_name: e.target.value })}
                                        required
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="semester">Current Semester</Label>
                                    <Input
                                        id="semester"
                                        type="number"
                                        min="1"
                                        max="8"
                                        placeholder="e.g., 5"
                                        value={formData.semester}
                                        onChange={(e) => setFormData({ ...formData, semester: e.target.value })}
                                        required
                                    />
                                </div>
                                <Button type="button" onClick={() => setStep(2)} className="w-full">
                                    Next
                                </Button>
                            </div>
                        )}

                        {step === 2 && (
                            <div className="space-y-4">
                                <h3 className="font-semibold text-lg">Academic Details</h3>
                                <div className="space-y-2">
                                    <Label htmlFor="subjects">Subjects (comma-separated)</Label>
                                    <Input
                                        id="subjects"
                                        placeholder="e.g., Computer Networks, DBMS, Web Development"
                                        value={formData.subjects}
                                        onChange={(e) => setFormData({ ...formData, subjects: e.target.value })}
                                        required
                                    />
                                    <p className="text-sm text-gray-500">Enter subjects separated by commas</p>
                                </div>
                                <div className="flex gap-2">
                                    <Button type="button" variant="outline" onClick={() => setStep(1)} className="flex-1">
                                        Back
                                    </Button>
                                    <Button type="button" onClick={() => setStep(3)} className="flex-1">
                                        Next
                                    </Button>
                                </div>
                            </div>
                        )}

                        {step === 3 && (
                            <div className="space-y-4">
                                <h3 className="font-semibold text-lg">Preferences</h3>
                                <div className="space-y-2">
                                    <Label>Preferred Language</Label>
                                    <div className="flex gap-4">
                                        <label className="flex items-center gap-2 cursor-pointer">
                                            <input
                                                type="radio"
                                                name="language"
                                                value="english"
                                                checked={formData.language === 'english'}
                                                onChange={(e) => setFormData({ ...formData, language: e.target.value })}
                                                className="w-4 h-4"
                                            />
                                            <span>English</span>
                                        </label>
                                        <label className="flex items-center gap-2 cursor-pointer">
                                            <input
                                                type="radio"
                                                name="language"
                                                value="hindi"
                                                checked={formData.language === 'hindi'}
                                                onChange={(e) => setFormData({ ...formData, language: e.target.value })}
                                                className="w-4 h-4"
                                            />
                                            <span>Hindi</span>
                                        </label>
                                    </div>
                                </div>
                                <div className="flex gap-2">
                                    <Button type="button" variant="outline" onClick={() => setStep(2)} className="flex-1">
                                        Back
                                    </Button>
                                    <Button type="submit" className="flex-1" disabled={loading}>
                                        {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                                        {!loading && <CheckCircle className="mr-2 h-4 w-4" />}
                                        Complete Setup
                                    </Button>
                                </div>
                            </div>
                        )}
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}
