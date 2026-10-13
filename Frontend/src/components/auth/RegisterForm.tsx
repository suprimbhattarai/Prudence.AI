import {
    useEffect,
    useState,
    type ChangeEvent,
    type FormEvent,
} from "react";

import { Link } from "react-router-dom";
import { LoaderCircle } from "lucide-react";

import { useAppDispatch, useAppSelector } from "../../app/hooks";

import {
    registerUserThunk,
    resetRegistrationState,
} from "../../features/auth/slices/authSlice";

import { fetchOrganizations } from "../../features/auth/slices/organizationSlice";

import type {
    RegisterRequest,
    RegistrationRole,
} from "../../features/auth/types/auth.types";

import PasswordInput from "../forms/PasswordInput";
import Loading from "../common/Loading";


interface RegisterFormProps {
    onRegistrationSuccess: (role: RegistrationRole) => void;
}

interface RegisterFormValues {
    full_name: string;
    email: string;
    phone: string;
    organization_id: string;
    role: RegistrationRole;
    password: string;
    confirm_password: string;
}

const initialFormValues: RegisterFormValues = {
    full_name: "",
    email: "",
    phone: "",
    organization_id: "",
    role: "customer",
    password: "",
    confirm_password: "",
};

const inputClassName = "w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm text-black outline-none transition-colors placeholder:text-gray-400 focus:border-black focus:ring-1 focus:ring-black disabled:cursor-not-allowed disabled:opacity-50";


export default function RegisterForm({
    onRegistrationSuccess,
}: RegisterFormProps) {
    const dispatch = useAppDispatch();

    const {
        loading: registrationLoading,
        success,
        error: registrationError,
    } = useAppSelector((state) => state.auth);

    const {
        organizations,
        loading: organizationsLoading,
        error: organizationsError,
    } = useAppSelector((state) => state.organizations);

    const [formData, setFormData] = useState<RegisterFormValues>(
        initialFormValues
    );

    const [validationError, setValidationError] = useState<string | null>(
        null
    );

    useEffect(() => {
        dispatch(resetRegistrationState());
        dispatch(fetchOrganizations());
    }, [dispatch]);


    function handleChange(
        event: ChangeEvent<HTMLInputElement | HTMLSelectElement>
    ) {
        const { name, value } = event.target;

        setFormData((previous) => ({
            ...previous,
            [name]: value,
        }));

        setValidationError(null);
    }


    function handleRoleChange(
        event: ChangeEvent<HTMLSelectElement>
    ) {
        const role = event.target.value;

        if (role !== "customer" && role !== "technician") {
            return;
        }

        setFormData((previous) => ({
            ...previous,
            role,
        }));

        setValidationError(null);
    }


    async function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();

        if (registrationLoading || success) {
            return;
        }

        setValidationError(null);

        if (formData.password.length < 12) {
            setValidationError(
                "Password must contain at least 12 characters."
            );
            return;
        }

        if (formData.password.length > 128) {
            setValidationError(
                "Password cannot exceed 128 characters."
            );
            return;
        }

        if (formData.password !== formData.confirm_password) {
            setValidationError("Passwords do not match.");
            return;
        }

        const selectedOrganization = organizations.find(
            (organization) =>
                organization.id === Number(formData.organization_id)
        );

        if (!selectedOrganization) {
            setValidationError("Please select a valid ISP.");
            return;
        }

        const payload: RegisterRequest = {
            full_name: formData.full_name.trim(),
            email: formData.email.trim(),
            phone: formData.phone.trim(),
            password: formData.password,
            organization_id: selectedOrganization.id,
            role: formData.role,
        };

        const result = await dispatch(registerUserThunk(payload));

        if (registerUserThunk.fulfilled.match(result)) {
            setFormData(initialFormValues);

            // Notify RegisterPage to open the universal SuccessModal.
            onRegistrationSuccess(payload.role);
        }
    }


    const isSubmittingDisabled =
        registrationLoading ||
        organizationsLoading ||
        organizations.length === 0 ||
        success;


    return (
        <form onSubmit={handleSubmit} className="space-y-5">

            <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">

                {/* Full name */}
                <div className="sm:col-span-2">
                    <label htmlFor="full_name" className="mb-2 block text-sm font-medium text-black">
                        Full name
                    </label>

                    <input
                        id="full_name"
                        name="full_name"
                        type="text"
                        autoComplete="name"
                        required
                        minLength={2}
                        maxLength={150}
                        placeholder="Enter your full name"
                        value={formData.full_name}
                        onChange={handleChange}
                        className={inputClassName}
                        disabled={registrationLoading || success}
                    />
                </div>

                {/* Email */}
                <div className="min-w-0">
                    <label htmlFor="email" className="mb-2 block text-sm font-medium text-black">
                        Email address
                    </label>

                    <input
                        id="email"
                        name="email"
                        type="email"
                        autoComplete="email"
                        required
                        placeholder="you@example.com"
                        value={formData.email}
                        onChange={handleChange}
                        className={inputClassName}
                        disabled={registrationLoading || success}
                    />
                </div>

                {/* Phone */}
                <div className="min-w-0">
                    <label htmlFor="phone" className="mb-2 block text-sm font-medium text-black">
                        Phone number
                    </label>

                    <input
                        id="phone"
                        name="phone"
                        type="tel"
                        autoComplete="tel"
                        maxLength={30}
                        placeholder="98XXXXXXXX"
                        value={formData.phone}
                        onChange={handleChange}
                        className={inputClassName}
                        disabled={registrationLoading || success}
                    />
                </div>

                {/* Organization */}
                <div className="sm:col-span-2">
                    <label htmlFor="organization_id" className="mb-2 block text-sm font-medium text-black">
                        Internet service provider
                    </label>

                    {organizationsLoading ? (
                        <Loading
                            variant="inline"
                            message="Loading available ISPs..."
                        />
                    ) : (
                        <select
                            id="organization_id"
                            name="organization_id"
                            required
                            value={formData.organization_id}
                            onChange={handleChange}
                            disabled={organizations.length === 0 || registrationLoading || success}
                            className={`${inputClassName} cursor-pointer disabled:cursor-not-allowed`}
                        >
                            <option value="">Select your ISP</option>

                            {organizations.map((organization) => (
                                <option key={organization.id} value={organization.id}>
                                    {organization.name} ({organization.code})
                                </option>
                            ))}
                        </select>
                    )}

                    {organizationsError && (
                        <div className="mt-3 space-y-2">
                            <p role="alert" className="text-sm text-red-700">
                                {organizationsError}
                            </p>

                            <button
                                type="button"
                                onClick={() => dispatch(fetchOrganizations())}
                                className="cursor-pointer text-sm font-medium text-black underline underline-offset-4 hover:text-gray-600"
                            >
                                Retry loading organizations
                            </button>
                        </div>
                    )}

                    {!organizationsLoading && !organizationsError && organizations.length === 0 && (
                        <p className="mt-2 text-sm text-gray-600">
                            No internet service providers are available.
                        </p>
                    )}
                </div>

                {/* Role */}
                <div className="sm:col-span-2">
                    <label htmlFor="role" className="mb-2 block text-sm font-medium text-black">
                        Register as
                    </label>

                    <select
                        id="role"
                        name="role"
                        required
                        value={formData.role}
                        onChange={handleRoleChange}
                        disabled={registrationLoading || success}
                        className={`${inputClassName} cursor-pointer disabled:cursor-not-allowed`}
                    >
                        <option value="customer">Customer</option>
                        <option value="technician">Technician</option>
                    </select>

                    {formData.role === "technician" && (
                        <div role="note" className="mt-3 rounded-lg border border-gray-200 bg-gray-50 px-4 py-3 text-sm leading-6 text-gray-700">
                            Technician accounts require administrator approval before accessing technician features.
                            Your employee code will be generated automatically by Prudence AI.
                        </div>
                    )}
                </div>

                {/* Password */}
                <div className="min-w-0">
                    <PasswordInput
                        id="password"
                        name="password"
                        label="Password"
                        placeholder="Minimum 12 characters"
                        value={formData.password}
                        onChange={handleChange}
                        disabled={registrationLoading || success}
                    />
                </div>

                {/* Confirm password */}
                <div className="min-w-0">
                    <PasswordInput
                        id="confirm_password"
                        name="confirm_password"
                        label="Confirm password"
                        placeholder="Repeat your password"
                        value={formData.confirm_password}
                        onChange={handleChange}
                        disabled={registrationLoading || success}
                    />
                </div>
            </div>

            {/* Validation and API errors */}
            {(validationError || registrationError) && (
                <div role="alert" className="rounded-lg border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-800">
                    {validationError || registrationError}
                </div>
            )}

            {/* Submit */}
            <button
                type="submit"
                disabled={isSubmittingDisabled}
                className="flex min-h-12 w-full cursor-pointer items-center justify-center gap-2 rounded-lg bg-black px-5 py-3 text-sm font-semibold text-white transition-colors hover:bg-gray-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-black disabled:cursor-not-allowed disabled:opacity-50"
            >
                {registrationLoading && (
                    <LoaderCircle
                        size={18}
                        className="animate-spin motion-reduce:animate-none"
                        aria-hidden="true"
                    />
                )}

                {registrationLoading
                    ? "Creating your account..."
                    : success
                        ? "Account created"
                        : "Create account"}
            </button>

            {/* Login link */}
            <p className="text-center text-sm text-gray-600">
                Already have an account?{" "}
                <Link
                    to="/login"
                    className="cursor-pointer font-semibold text-black underline-offset-4 hover:underline focus-visible:outline-2 focus-visible:outline-offset-2"
                >
                    Log in
                </Link>
            </p>
        </form>
    );
}