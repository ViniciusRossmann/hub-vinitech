import type { Metadata } from 'next';
import { Geist, Geist_Mono } from 'next/font/google';
import './globals.css';

const geistSans = Geist({
	variable: '--font-geist-sans',
	subsets: ['latin'],
});

const geistMono = Geist_Mono({
	variable: '--font-geist-mono',
	subsets: ['latin'],
});

export const metadata: Metadata = {
	title: 'Vinícius Rossmann Nunes - Software Engineer',
	description:
		'A passionate developer who believes in simplicity and effectiveness.',
	icons: {
		icon: '/code.ico'
	},
	keywords: [
		'Software Developer',
		'Software Engineer',
		'Software Architecture',
		'C#',
		'.NET',
		'TypeScript',
		'Angular',
		'Node.js',
		'Problem Solving',
		'Effective Solutions',
		'Web Development',
		'Frontend Development',
		'Backend Development',
		'Full Stack Development',
		'Cloud Computing',
		'AWS',
		'Kafka',
		'Microservices',
		'APIs',
		'Clean Code',
		'Vinicius Rossmann Nunes',
		'Vinicius Nunes'
	],
	authors: [{ name: 'Vinícius Rossmann Nunes' }],
	creator: 'Vinícius Rossmann Nunes',
	openGraph: {
		title: 'Vinícius Rossmann Nunes - Software Engineer',
		description: 'Passionate developer creating simple and effective solutions. Explore my projects and development approach.',
		url: 'https://viniciusnunes.tech',
		siteName: 'Vinícius Rossmann Nunes - Software Engineer',
		images: [
			{
				url: '/og-image.jpg',
				width: 1200,
				height: 630,
				alt: 'Vinícius Rossmann Nunes - Software Engineer',
			},
		],
		locale: 'en_US',
		type: 'website',
	},
	twitter: {
		card: 'summary_large_image',
		title: 'Vinícius Rossmann Nunes - Software Engineer',
		description: 'Passionate developer creating simple and effective solutions. Explore my projects and development approach.',
		creator: '@viniciurossmann',
		images: ['/og-image.jpg'],
	},
	robots: {
		index: true,
		follow: true,
		googleBot: {
			index: true,
			follow: true,
			'max-video-preview': -1,
			'max-image-preview': 'large',
			'max-snippet': -1,
		},
	},
};

export default function RootLayout({
	children,
}: Readonly<{
	children: React.ReactNode;
}>) {
	return (
		<html lang="en">
			<body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>{children}</body>
		</html>
	);
}
