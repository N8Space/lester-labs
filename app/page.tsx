import Link from "next/link";
import { Card } from "@/components/ui/Card";
import { GridBackground } from "@/components/layout/GridBackground";
import { ShoppingBag, Terminal } from "lucide-react";

export default function Home() {
  return (
    <GridBackground>
      {/* Navigation */}
      <nav className="fixed top-6 left-1/2 -translate-x-1/2 z-50">
        <div className="bg-white/90 backdrop-blur-sm px-6 py-3 rounded-full shadow-sm border border-stone-200 flex gap-6 text-sm font-medium text-stone-600">
          <Link href="/projects" className="hover:text-stone-900 transition-colors">
            Projects
          </Link>
          <Link href="/shop" className="hover:text-stone-900 transition-colors">
            Shop
          </Link>
          <Link href="/about" className="hover:text-stone-900 transition-colors">
            About
          </Link>
        </div>
      </nav>

      <main className="flex flex-col items-center justify-center min-h-screen p-4 relative overflow-hidden">

        {/* Main Title Card -> Now Logo Image */}
        <div className="z-10 relative">
          <img
            src="/logo.png"
            alt="Lester Labs"
            className="w-full max-w-lg drop-shadow-sm"
          />
        </div>

        {/* Sticky Note: Shop (Moved further left/top) */}
        <Link href="/shop" className="absolute top-[10%] left-[2%] md:left-[10%] z-20 hover:z-30 block group">
          <div className="bg-gradient-to-br from-yellow-100 to-yellow-200 text-stone-900 p-6 w-48 h-48 md:w-56 md:h-56 shadow-[2px_10px_20px_rgba(0,0,0,0.15)] -rotate-6 group-hover:-rotate-3 transition-all duration-300 font-hand text-2xl flex flex-col items-center justify-center leading-tight text-center relative after:content-[''] after:absolute after:bottom-1 after:right-1 after:w-full after:h-full after:bg-black/5 after:blur-md after:-z-10 rounded-sm">
            {/* Tape effect (Optional, can add later) */}
            <span className="relative z-10">Check out the Shop!</span>
            <ShoppingBag className="w-10 h-10 mt-3 opacity-80 relative z-10" />
          </div>
        </Link>

        {/* Decorative Product Card: Sample (Moved further right/top) */}
        <div className="absolute top-[15%] right-[2%] md:right-[15%] z-30 pointer-events-none">
          <img
            src="/stickers.png"
            alt="Cute Stickers"
            className="w-40 h-40 md:w-48 md:h-48 rotate-6 drop-shadow-md mix-blend-multiply"
          />
        </div>

        {/* Code Card: Projects (Moved further bottom/right) */}
        <Link href="/projects" className="absolute bottom-[5%] right-[2%] md:right-[10%] z-20 hover:z-30 block">
          <Card
            className="bg-stone-900 text-stone-50 border-stone-800 w-64 md:w-72 rotate-2 hover:rotate-0 transition-all duration-300 p-0 overflow-hidden shadow-xl"
            whileHover={{ scale: 1.05, rotate: 0 }}
          >
            {/* MacOS Window Controls */}
            <div className="bg-stone-800 px-4 py-3 flex gap-2 border-b border-stone-700">
              <div className="w-3 h-3 rounded-full bg-red-500" />
              <div className="w-3 h-3 rounded-full bg-yellow-500" />
              <div className="w-3 h-3 rounded-full bg-green-500" />
            </div>
            <div className="p-6 font-mono text-sm text-green-400">
              <p className="mb-2 opacity-50 text-xs">user@lester-labs:~</p>
              <p>&gt; np run projects</p>
              <p className="text-stone-400 mt-2">{"//"} Explore AI & Code</p>
              <Terminal className="w-10 h-10 mt-6 text-white opacity-80" />
            </div>
          </Card>
        </Link>

      </main>
    </GridBackground>
  );
}
