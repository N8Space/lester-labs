import React from 'react';

export default function PrivacyPolicy() {
    return (
        <div className="min-h-screen bg-neutral-950 text-neutral-200 py-20 px-6">
            <div className="max-w-3xl mx-auto glass-card p-8 md:p-12 rounded-2xl">
                <h1 className="text-3xl md:text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-teal-400 to-indigo-500 mb-8">
                    Privacy Policy
                </h1>
                <p className="text-sm text-neutral-400 mb-8">Last Updated: February 24, 2026</p>

                <div className="space-y-8 text-neutral-300 leading-relaxed">
                    <section>
                        <h2 className="text-xl font-semibold text-white mb-4">1. Information We Collect</h2>
                        <p>
                            Lester Labs and our associated applications (including &quot;Resume Refine&quot;) are designed to minimize data collection. We collect the following information provided by you to furnish our core generative services:
                        </p>
                        <ul className="list-disc pl-6 mt-4 space-y-2">
                            <li>Public LinkedIn Profile URLs</li>
                            <li>Public Job Posting URLs</li>
                            <li>Text input fields necessary to complete missing professional data (e.g., Phone Number, Email, Skills)</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold text-white mb-4">2. How We Use and Process Data (AI Disclosure)</h2>
                        <p className="mb-4">
                            The data you provide is sent securely to our proprietary API servers and processed using artificial intelligence (including Google Gemini LLMs).
                        </p>
                        <ul className="list-disc pl-6 space-y-2">
                            <li>We use the provided data strictly for the purpose of generating ATS-optimized resumes and tailored cover letters.</li>
                            <li>We do <strong>not</strong> use your data to train our own AI models.</li>
                            <li>The generated documents are returned directly to your device.</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold text-white mb-4">3. Data Retention</h2>
                        <p>
                            Our systems process your requests ephemerally in real-time. We do not permanently store your LinkedIn profile data, job postings, or the resulting generated resumes on our servers after the session is complete. The generated documents are stored locally on your device and remain under your complete control.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold text-white mb-4">4. App Tracking Transparency</h2>
                        <p>
                            We do <strong>not</strong> track your activity across other companies&apos; apps or websites. We do not use third-party advertising SDKs (such as Meta Ads or Google AdMob) that collect device identifiers (IDFA) for targeted advertising.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold text-white mb-4">5. Contact Us</h2>
                        <p>
                            If you have any questions about this Privacy Policy, please contact us at: <a href="mailto:nathan@lesterlabs.cloud" className="text-teal-400 hover:text-teal-300 transition-colors">support@lesterlabs.cloud</a>
                        </p>
                    </section>
                </div>
            </div>
        </div>
    );
}
