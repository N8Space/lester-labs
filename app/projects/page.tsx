import Link from "next/link";
import { GridBackground } from "@/components/layout/GridBackground";
import { Card } from "@/components/ui/Card";
import { ArrowLeft } from "lucide-react";

export default function ProjectsPage() {
    return (
        <GridBackground>
            <div className="container mx-auto p-8">
                <Link href="/" className="inline-flex items-center gap-2 text-stone-500 hover:text-stone-900 mb-8 transition-colors">
                    <ArrowLeft size={20} /> Back to Hub
                </Link>
                <h1 className="text-4xl font-bold mb-8">Projects</h1>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {/* Vokome Project Card */}
                    <Link href="https://vokome.lesterlabs.cloud" className="group relative block h-64 rounded-xl overflow-hidden shadow-2xl hover:shadow-cyan-500/20 transition-all duration-500 hover:-translate-y-2">
                        {/* Background Image */}
                        <div className="absolute inset-0 z-0">
                            <img
                                src="/vokome-card-bg.png"
                                alt="Vokome Background"
                                className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                            />
                            <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent mix-blend-multiply" />
                            <div className="absolute inset-0 bg-cyan-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                        </div>

                        {/* Content Overlay */}
                        <div className="relative z-10 h-full flex flex-col justify-end p-6 border border-white/10 rounded-xl group-hover:border-cyan-400/50 transition-colors duration-300">
                            <div className="transform translate-y-2 group-hover:translate-y-0 transition-transform duration-300">
                                <h2 className="text-3xl font-black text-white mb-2 tracking-tight drop-shadow-[0_2px_4px_rgba(0,0,0,0.8)] group-hover:text-cyan-400 transition-colors">
                                    Vokome
                                </h2>
                                <p className="text-stone-300 font-medium text-sm mb-4 opacity-80 group-hover:opacity-100">
                                    AI-Powered Video / Audio Generator
                                </p>
                                <div className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-cyan-400 opacity-0 group-hover:opacity-100 transition-all duration-300 -translate-x-4 group-hover:translate-x-0">
                                    Launch App <span>→</span>
                                </div>
                            </div>
                        </div>
                    </Link>

                    {/* Placeholders for other projects */}
                    {[2, 3].map((i) => (
                        <Card key={i} className="h-64 flex items-center justify-center text-stone-400 bg-stone-100/50 border-dashed border-stone-300">
                            <span className="text-sm font-medium">Coming Soon {i}</span>
                        </Card>
                    ))}
                </div>
            </div>
        </GridBackground>
    );
}
