import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

import logo from "../../assets/logo/logo.png";

import RegisterForm from "../../components/auth/RegisterForm";
import SuccessModal from "../../components/common/SuccessModal";

import type { RegistrationRole } from "../../features/auth/types/auth.types";

export default function RegisterPage() {
    const navigate = useNavigate();

    const [registeredRole, setRegisteredRole] = useState<RegistrationRole | null>(null);

    function handleRegistrationSuccess(role: RegistrationRole) {
        setRegisteredRole(role);
    }

    const isTechnician = registeredRole === "technician";

    return (
        <>
            <main className="min-h-dvh bg-white px-4 py-6 text-black sm:px-6 sm:py-10 lg:px-8">
                <div className="mx-auto w-full max-w-xl">
                    <Link
                        to="/"
                        className="mb-8 inline-flex cursor-pointer items-center gap-2 rounded-md text-sm font-medium text-gray-600 transition-colors hover:text-black focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-black"
                    >
                        <ArrowLeft size={18} aria-hidden="true" />
                        Back to explore
                    </Link>

                    <div className="mb-8 text-center">
                        <Link
                            to="/"
                            aria-label="Go to Prudence AI home"
                            className="inline-block cursor-pointer rounded-lg focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-black"
                        >
                            <img
                                src={logo}
                                alt="Prudence AI"
                                className="mx-auto mb-5 h-20 w-20 object-contain sm:h-24 sm:w-24"
                            />
                        </Link>

                        <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">
                            Create your account
                        </h1>

                        <p className="mx-auto mt-3 max-w-sm text-sm leading-6 text-gray-600">
                            Register to manage your internet service,
                            report issues, and track support requests.
                        </p>
                    </div>

                    <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm sm:p-8">
                        <RegisterForm onRegistrationSuccess={handleRegistrationSuccess} />
                    </div>

                    <footer className="mt-8 text-center">
                        <p className="text-xs text-gray-500">
                            © {new Date().getFullYear()} Prudence AI.
                            All rights reserved.
                        </p>
                    </footer>
                </div>
            </main>

            <SuccessModal
                open={registeredRole !== null}
                title="Registration Successful!"
                message={
                    isTechnician
                        ? "Your technician account has been created successfully. Please wait for administrator approval before logging in."
                        : "Your customer account has been created successfully. You can now log in to Prudence AI."
                }
                description={
                    isTechnician
                        ? "Account status: Pending administrator approval"
                        : undefined
                }
                primaryAction={{
                    label: "Go to Login",
                    onClick: () => navigate("/login"),
                }}
                secondaryAction={{
                    label: "Go to Home",
                    onClick: () => navigate("/"),
                }}
            />
        </>
    );
}