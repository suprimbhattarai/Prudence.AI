import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

import logo from "../../assets/logo/logo.png";

import LoginForm from "../../components/auth/LoginForm";

export default function LoginPage() {
    return (
        <main className="flex min-h-dvh flex-col bg-white px-4 py-6 text-black sm:px-6 sm:py-10 lg:px-8">
            <div className="mx-auto w-full max-w-md">
                <Link
                    to="/"
                    className="mb-10 inline-flex cursor-pointer items-center gap-2 rounded-md text-sm font-medium text-gray-600 transition-colors hover:text-black focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-black"
                >
                    <ArrowLeft size={18} aria-hidden="true" />
                    Back to explore
                </Link>

                <div className="mb-8 text-center">
                    <Link to="/" aria-label="Prudence AI home" className="inline-block cursor-pointer rounded-lg">
                        <img src={logo} alt="Prudence AI" className="mx-auto mb-5 h-24 w-24 object-contain" />
                    </Link>

                    <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">
                        Welcome back
                    </h1>

                    <p className="mt-3 text-sm leading-6 text-gray-600">
                        Log in to your Prudence AI account.
                    </p>
                </div>

                <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm sm:p-8">
                    <LoginForm />
                </div>

                <footer className="mt-8 text-center text-xs text-gray-500">
                    © {new Date().getFullYear()} Prudence AI. All rights reserved.
                </footer>
            </div>
        </main>
    );
}