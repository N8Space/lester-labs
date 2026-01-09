import Link from "next/link";
import { GridBackground } from "@/components/layout/GridBackground";
import { Card } from "@/components/ui/Card";
import { ArrowLeft } from "lucide-react";

export default function ShopPage() {
    return (
        <GridBackground>
            <div className="container mx-auto p-8">
                <Link href="/" className="inline-flex items-center gap-2 text-stone-500 hover:text-stone-900 mb-8 transition-colors">
                    <ArrowLeft size={20} /> Back to Hub
                </Link>
                <h1 className="text-4xl font-bold mb-8 font-hand">The Shop</h1>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {[1, 2, 3].map((i) => (
                        <Card key={i} className="h-80 flex flex-col items-center justify-center text-stone-400">
                            <div className="w-32 h-32 bg-stone-100 rounded-lg mb-4" />
                            <p>Product Placeholder {i}</p>
                        </Card>
                    ))}
                </div>
            </div>
        </GridBackground>
    );
}
