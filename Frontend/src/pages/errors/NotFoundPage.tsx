import { Link } from "react-router-dom";
import { ArrowLeft, House } from "lucide-react";

import logo from "../../assets/logo/logo.png";

export default function NotFoundPage() {
    return (
        <main className="flex min-h-dvh items-center justify-center bg-white px-4 py-10 text-black sm:px-6 lg:px-8">
            <div className="w-full max-w-lg text-center">

                {/* Prudence AI logo */}
                <Link
                    to="/"
                    aria-label="Prudence AI home"
                    className="inline-block cursor-pointer rounded-lg focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-black"
                >
                    <img
                        src={logo}
                        alt="Prudence AI"
                        className="mx-auto h-20 w-20 object-contain sm:h-24 sm:w-24"
                    />
                </Link>

                {/* Error code */}
                <div className="mt-8">
                    <h1 className="text-7xl font-bold tracking-tight text-black sm:text-8xl lg:text-9xl">
                        404
                    </h1>

                    <div className="mx-auto mt-5 h-1 w-16 rounded-full bg-black" />

                    <h2 className="mt-7 text-2xl font-bold tracking-tight sm:text-3xl">
                        Page Not Found
                    </h2>

                    <p className="mx-auto mt-4 max-w-sm text-sm leading-6 text-gray-600 sm:text-base">
                        Sorry, the page you're looking for doesn't exist
                        or may have been moved.
                    </p>
                </div>

                {/* Home navigation */}
                <div className="mt-9 flex justify-center">
                    <Link
                        to="/"
                        className="inline-flex min-h-12 w-full cursor-pointer items-center justify-center gap-2 rounded-lg bg-black px-8 py-3 text-sm font-semibold text-white transition-colors hover:bg-gray-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-black sm:w-auto"
                    >
                        <House size={18} aria-hidden="true" />
                        Go to Home
                    </Link>
                </div>

                {/* Back navigation */}
                <button
                    type="button"
                    onClick={() => window.history.back()}
                    className="mt-5 inline-flex cursor-pointer items-center gap-2 rounded-md text-sm font-medium text-gray-500 transition-colors hover:text-black focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-black"
                >
                    <ArrowLeft size={16} aria-hidden="true" />
                    Go back
                </button>

                {/* Footer */}
                <footer className="mt-16 text-xs text-gray-500">
                    © {new Date().getFullYear()} Prudence AI. All rights reserved.
                </footer>
            </div>
        </main>
    );
}