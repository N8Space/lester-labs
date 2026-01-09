"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface CardProps {
    children: React.ReactNode;
    className?: string;
    rotate?: number;
    whileHover?: object;
}

export function Card({ children, className, rotate = 0, whileHover }: CardProps) {
    return (
        <motion.div
            initial={{ rotate: rotate }}
            whileHover={
                whileHover || {
                    scale: 1.02,
                    rotate: 0,
                    boxShadow: "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)",
                }
            }
            className={cn(
                "bg-white rounded-2xl shadow-md p-6 border border-stone-100",
                className
            )}
        >
            {children}
        </motion.div>
    );
}
