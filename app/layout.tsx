import type { Metadata } from "next";
import { Inter, Kalam } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

const kalam = Kalam({
  weight: ["300", "400", "700"],
  subsets: ["latin"],
  variable: "--font-kalam",
});

export const metadata: Metadata = {
  title: "Lester Labs",
  description: "A Hub for AI, Code, & Family Creations",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${inter.variable} ${kalam.variable} antialiased bg-stone-50 text-stone-900`}
      >
        {children}
      </body>
    </html>
  );
}
