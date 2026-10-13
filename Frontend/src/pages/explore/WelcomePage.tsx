import { Link, useNavigate } from "react-router-dom";
import { LogOut, ShieldCheck, UserRound, Building2 } from "lucide-react";

import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { logout } from "../../features/auth/slices/authSlice";
import { tokenStore } from "../../features/auth/services/tokenStore";

import logo from "../../assets/logo/logo.png";

export default function WelcomePage() {
    const dispatch = useAppDispatch();
    const navigate = useNavigate();

    const user = useAppSelector((state) => state.auth.user);

    function handleLogout() {
        tokenStore.clearTokens();
        dispatch(logout());
        navigate("/login", { replace: true });
    }

    if (!user) {
        return null;
    }

    const displayRole = user.role.charAt(0).toUpperCase() + user.role.slice(1);

    return (
        <div className="min-h-dvh bg-white text-black">
            <header className="border-b border-gray-200">
                <nav className="mx-auto flex w-full max-w-6xl flex-wrap items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
                    <Link to="/" className="flex cursor-pointer items-center gap-3">
                        <img src={logo} alt="" className="h-11 w-11 object-contain" />
                        <span className="text-lg font-bold tracking-tight">Prudence AI</span>
                    </Link>

                    <button
                        type="button"
                        onClick={handleLogout}
                        className="inline-flex min-h-11 cursor-pointer items-center gap-2 rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium transition-colors hover:bg-gray-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-black"
                    >
                        <LogOut size={17} aria-hidden="true" />
                        Log out
                    </button>
                </nav>
            </header>

            <main className="mx-auto w-full max-w-4xl px-4 py-12 sm:px-6 sm:py-20">
                <div className="mb-10 text-center">
                    <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-full bg-gray-100">
                        <ShieldCheck size={32} className="text-black" aria-hidden="true" />
                    </div>

                    <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
                        Welcome to Prudence AI!
                    </h1>

                    <p className="mt-3 text-sm leading-6 text-gray-600 sm:text-base">
                        You have successfully logged in to your account.
                    </p>
                </div>

                <section className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm sm:p-8">
                    <div className="mb-6 flex items-center gap-3">
                        <UserRound size={22} aria-hidden="true" />
                        <h2 className="text-xl font-semibold">Your account</h2>
                    </div>

                    <dl className="divide-y divide-gray-100">
                        <div className="flex flex-wrap items-center justify-between gap-2 py-4">
                            <dt className="text-sm text-gray-500">Email</dt>
                            <dd className="min-w-0 break-all text-sm font-medium">{user.email}</dd>
                        </div>

                        <div className="flex items-center justify-between gap-2 py-4">
                            <dt className="text-sm text-gray-500">Role</dt>
                            <dd className="text-sm font-medium">{displayRole}</dd>
                        </div>

                        <div className="flex items-center justify-between gap-2 py-4">
                            <dt className="inline-flex items-center gap-2 text-sm text-gray-500">
                                <Building2 size={16} aria-hidden="true" />
                                Organization ID
                            </dt>
                            <dd className="text-sm font-medium">{user.organization_id}</dd>
                        </div>

                        <div className="flex items-center justify-between gap-2 py-4">
                            <dt className="text-sm text-gray-500">Account status</dt>
                            <dd className="text-sm font-medium">{user.is_active ? "Active" : "Inactive"}</dd>
                        </div>

                        <div className="flex items-center justify-between gap-2 py-4">
                            <dt className="text-sm text-gray-500">Verification</dt>
                            <dd className="text-sm font-medium">{user.is_verified ? "Verified" : "Pending"}</dd>
                        </div>
                    </dl>
                </section>

                <div className="mt-6 rounded-xl border border-gray-200 bg-gray-50 p-5 text-center">
                    <h2 className="text-base font-semibold">Your Prudence AI workspace</h2>
                    <p className="mt-2 text-sm leading-6 text-gray-600">
                        This is a temporary welcome page. Your role-specific dashboard, support tickets, and service tools will be implemented next.
                    </p>
                </div>
            </main>
        </div>
    );
}