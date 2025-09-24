'use client';

import HeroSection from './components/HeroSection';
import ContactSection from './components/ContactSection';

export default function SimplePortfolio() {
	return (
		<main className="min-h-screen bg-white pt-12">
			<HeroSection />
			<ContactSection />
		</main>
	);
}
