import HeroSection from '@/components/landing/HeroSection';
import FeaturesSection from '@/components/landing/FeaturesSection';
import PricingSection from '@/components/landing/PricingSection';

export default function HomePage() {
    return (
        <main className="min-h-screen">
            <HeroSection />
            <FeaturesSection />
            <PricingSection />

            {/* Footer */}
            <footer className="bg-gray-900 text-white py-12">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
                        <div>
                            <h3 className="text-xl font-bold mb-4">SubmitWise</h3>
                            <p className="text-gray-400">
                                AI-powered college project generator for Indian students
                            </p>
                        </div>
                        <div>
                            <h4 className="font-semibold mb-4">Product</h4>
                            <ul className="space-y-2 text-gray-400">
                                <li><a href="#features" className="hover:text-white">Features</a></li>
                                <li><a href="#pricing" className="hover:text-white">Pricing</a></li>
                                <li><a href="/docs" className="hover:text-white">Documentation</a></li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="font-semibold mb-4">Company</h4>
                            <ul className="space-y-2 text-gray-400">
                                <li><a href="/about" className="hover:text-white">About</a></li>
                                <li><a href="/contact" className="hover:text-white">Contact</a></li>
                                <li><a href="/careers" className="hover:text-white">Careers</a></li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="font-semibold mb-4">Legal</h4>
                            <ul className="space-y-2 text-gray-400">
                                <li><a href="/privacy" className="hover:text-white">Privacy Policy</a></li>
                                <li><a href="/terms" className="hover:text-white">Terms of Service</a></li>
                            </ul>
                        </div>
                    </div>
                    <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
                        <p>&copy; 2024 SubmitWise. All rights reserved.</p>
                    </div>
                </div>
            </footer>
        </main>
    );
}
