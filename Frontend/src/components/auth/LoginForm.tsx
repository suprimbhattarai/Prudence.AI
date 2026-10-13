import {
    useEffect,
    useState,
    type ChangeEvent,
    type FormEvent,
} from "react";

import {
    Link,
    useLocation,
    useNavigate,
} from "react-router-dom";

import { LoaderCircle } from "lucide-react";

import { useAppDispatch, useAppSelector } from "../../app/hooks";

import {
    clearLoginError,
    loginUserThunk,
} from "../../features/auth/slices/authSlice";

import PasswordInput from "../forms/PasswordInput";

interface LoginFormValues {
    email: string;
    password: string;
}

const initialFormValues: LoginFormValues = {
    email: "",
    password: "",
};

export default function LoginForm() {
    const dispatch = useAppDispatch();
    const navigate = useNavigate();
    const location = useLocation();

    const { loginLoading, loginError } = useAppSelector(
        (state) => state.auth
    );

    const [formData, setFormData] = useState<LoginFormValues>(
        initialFormValues
    );

    useEffect(() => {
        dispatch(clearLoginError());
    }, [dispatch]);

    function handleChange(event: ChangeEvent<HTMLInputElement>) {
        const { name, value } = event.target;

        setFormData((previous) => ({
            ...previous,
            [name]: value,
        }));
    }

    async function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();

        if (loginLoading) {
            return;
        }

        const result = await dispatch(
            loginUserThunk({
                email: formData.email.trim().toLowerCase(),
                password: formData.password,
            })
        );

        if (loginUserThunk.fulfilled.match(result)) {
            setFormData(initialFormValues);

            const requestedPath =
                (location.state as { from?: { pathname?: string } } | null)
                    ?.from?.pathname;

            const destination =
                requestedPath &&
                    requestedPath.startsWith("/") &&
                    !requestedPath.startsWith("//") &&
                    requestedPath !== "/login" &&
                    requestedPath !== "/register"
                    ? requestedPath
                    : "/welcome";

            navigate(destination, { replace: true });
        }
    }

    return (
        <form onSubmit={handleSubmit} className="space-y-5">
            <div>
                <label htmlFor="login-email" className="mb-2 block text-sm font-medium text-black">
                    Email address
                </label>

                <input
                    id="login-email"
                    name="email"
                    type="email"
                    autoComplete="email"
                    required
                    autoFocus
                    placeholder="you@example.com"
                    value={formData.email}
                    onChange={handleChange}
                    disabled={loginLoading}
                    className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm text-black outline-none transition-colors placeholder:text-gray-400 focus:border-black focus:ring-1 focus:ring-black disabled:cursor-not-allowed disabled:opacity-50"
                />
            </div>

            <PasswordInput
                id="login-password"
                name="password"
                label="Password"
                placeholder="Enter your password"
                value={formData.password}
                onChange={handleChange}
                minLength={1}
                autoComplete="current-password"
                disabled={loginLoading}
            />

            {loginError && (
                <div role="alert" className="rounded-lg border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-800">
                    {loginError}
                </div>
            )}

            <button
                type="submit"
                disabled={loginLoading}
                className="flex min-h-12 w-full cursor-pointer items-center justify-center gap-2 rounded-lg bg-black px-5 py-3 text-sm font-semibold text-white transition-colors hover:bg-gray-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-black disabled:cursor-not-allowed disabled:opacity-50"
            >
                {loginLoading && (
                    <LoaderCircle
                        size={18}
                        className="animate-spin motion-reduce:animate-none"
                        aria-hidden="true"
                    />
                )}

                {loginLoading ? "Signing in..." : "Log in"}
            </button>

            <p className="text-center text-sm text-gray-600">
                Don't have an account?{" "}
                <Link
                    to="/register"
                    className="cursor-pointer font-semibold text-black underline-offset-4 hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-black"
                >
                    Create account
                </Link>
            </p>
        </form>
    );
}