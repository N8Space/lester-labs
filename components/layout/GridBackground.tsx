export function GridBackground({ children }: { children: React.ReactNode }) {
    return (
        <div className="min-h-screen w-full relative overflow-hidden bg-stone-50">
            {/* Photorealistic Workshop Background */}
            <div className="absolute inset-0 z-0">
                <img
                    src="/background.png"
                    alt="Workshop Desk Background"
                    className="w-full h-full object-cover opacity-90"
                />
                {/* White overlay to ensure text readability if needed, or vignette */}
                <div className="absolute inset-0 bg-white/10" />
            </div>

            {/* Content wrapper */}
            <div className="relative z-10 w-full min-h-screen">
                {children}
            </div>
        </div>
    );
}
