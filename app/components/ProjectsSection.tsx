import Image from 'next/image';

export default function ProjectsSection() {
	return (
		<section className="py-12 sm:py-20">
			<div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
				<h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-6 sm:mb-8 text-center">Featured Projects</h2>
				<div className="grid grid-cols-1 sm:grid-cols-2 gap-6 sm:gap-8">
					<div key="project-1" className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
						<div className="aspect-video bg-gray-100 relative">
							<Image src={`/code.jpg`} alt="Project 1" fill className="object-cover" />
						</div>
						<div className="p-4 sm:p-6">
							<h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-2">Project Title 1</h3>
							<p className="text-sm sm:text-base text-gray-600 mb-4">A brief description of the project and the technologies used in its development.</p>
							<div className="flex gap-2">
								<a href="#" className="text-blue-600 hover:text-blue-800 font-medium text-sm sm:text-base">
									View Project →
								</a>
							</div>
						</div>
					</div>
					<div key="project-2" className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
						<div className="aspect-video bg-gray-100 relative">
							<Image src={`/code.jpg`} alt="Project 2" fill className="object-cover" />
						</div>
						<div className="p-4 sm:p-6">
							<h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-2">Project Title 2</h3>
							<p className="text-sm sm:text-base text-gray-600 mb-4">A brief description of the project and the technologies used in its development.</p>
							<div className="flex gap-2">
								<a href="#" className="text-blue-600 hover:text-blue-800 font-medium text-sm sm:text-base">
									View Project →
								</a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</section>
	);
}
