import { Link } from "react-router-dom";

import {
    ArrowRight,
    Headset,
    CalendarDays,
    ClipboardList,
    Wifi,
} from "lucide-react";

import logo from "../../assets/logo/logo.png";

const features = [
    {
        title: "AI Support",
        description: "Get help understanding and troubleshooting internet issues.",
        icon: Headset,
    },
    {
        title: "Ticket Management",
        description: "Report problems and track support requests.",
        icon: ClipboardList,
    },
    {
        title: "Technician Visits",
        description: "Manage service appointments and technician visits.",
        icon: CalendarDays,
    },
    {
        title: "Internet Services",
        description: "Access your ISP service and support information.",
        icon: Wifi,
    },
];

export default function ExplorePage() {
    return (
        <div className="min-h-dvh bg-white text-black">
            <header className="border-b border-gray-200">
                <nav
                    aria-label="Main navigation"
                    className="
                        mx-auto flex w-full max-w-7xl
                        flex-wrap items-center justify-between gap-3
                        px-4 py-4 sm:px-6 lg:px-8
                    "
                >
                    <Link
                        to="/"
                        className="flex cursor-pointer items-center gap-3"
                    >
                        <img
                            src={logo}
                            alt=""
                            className="h-11 w-11 object-contain"
                        />

                        <span className="text-lg font-bold tracking-tight">
                            Prudence AI
                        </span>
                    </Link>

                    <div className="flex items-center gap-2 sm:gap-4">
                        <Link
                            to="/login"
                            className="
                                cursor-pointer rounded-lg px-3 py-2
                                text-sm font-medium transition
                                hover:bg-gray-100
                            "
                        >
                            Log in
                        </Link>

                        <Link
                            to="/register"
                            className="
                                cursor-pointer rounded-lg bg-black
                                px-4 py-2.5 text-sm font-medium
                                text-white transition hover:bg-gray-800
                            "
                        >
                            Get Started
                        </Link>
                    </div>
                </nav>
            </header>

            <main>
                <section className="mx-auto max-w-7xl px-4 py-20 text-center sm:px-6 sm:py-28 lg:px-8">
                    <span className="inline-block rounded-full border border-gray-200 px-4 py-2 text-xs font-medium text-gray-600">
                        AI-Powered Customer Support
                    </span>

                    <h1 className="mx-auto mt-7 max-w-3xl text-4xl font-bold tracking-tight sm:text-5xl lg:text-6xl">
                        Smarter support.
                        <span className="block text-gray-500">
                            Better service.
                        </span>
                    </h1>

                    <p className="mx-auto mt-6 max-w-xl text-base leading-7 text-gray-600 sm:text-lg">
                        Prudence AI brings internet service support,
                        issue tracking, and technician coordination
                        into one platform.
                    </p>

                    <div className="mt-9 flex flex-col items-center justify-center gap-3 sm:flex-row">
                        <Link
                            to="/register"
                            className="
                                inline-flex min-h-12 w-full cursor-pointer
                                items-center justify-center gap-2
                                rounded-lg bg-black px-7 py-3
                                text-sm font-semibold text-white
                                transition hover:bg-gray-800 sm:w-auto
                            "
                        >
                            Create Account
                            <ArrowRight size={18} aria-hidden="true" />
                        </Link>

                        <Link
                            to="/login"
                            className="
                                inline-flex min-h-12 w-full cursor-pointer
                                items-center justify-center
                                rounded-lg border border-gray-300
                                px-7 py-3 text-sm font-semibold
                                transition hover:bg-gray-100 sm:w-auto
                            "
                        >
                            Log In
                        </Link>
                    </div>
                </section>

                <section className="border-t border-gray-100 bg-gray-50 py-16 sm:py-20">
                    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                        <div className="mb-10 text-center">
                            <h2 className="text-2xl font-bold sm:text-3xl">
                                One platform for better support
                            </h2>

                            <p className="mt-3 text-sm text-gray-600">
                                The capabilities we're building for ISP customers.
                            </p>
                        </div>

                        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
                            {features.map((feature) => {
                                const Icon = feature.icon;

                                return (
                                    <article
                                        key={feature.title}
                                        className="
                                            rounded-xl border border-gray-200
                                            bg-white p-6
                                        "
                                    >
                                        <div className="mb-5 flex h-11 w-11 items-center justify-center rounded-lg bg-gray-100">
                                            <Icon
                                                size={22}
                                                aria-hidden="true"
                                            />
                                        </div>

                                        <h3 className="text-base font-semibold">
                                            {feature.title}
                                        </h3>

                                        <p className="mt-2 text-sm leading-6 text-gray-600">
                                            {feature.description}
                                        </p>
                                    </article>
                                );
                            })}
                        </div>
                    </div>
                </section>
            </main>

            <footer className="border-t border-gray-200 px-4 py-6 text-center text-xs text-gray-500">
                © {new Date().getFullYear()} Prudence AI
            </footer>
        </div>
    );
}