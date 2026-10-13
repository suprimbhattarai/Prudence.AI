import { useState, type ChangeEvent } from "react";
import { Eye, EyeOff } from "lucide-react";

interface PasswordInputProps {
    id: string;
    name: string;
    label: string;
    value: string;
    onChange: (event: ChangeEvent<HTMLInputElement>) => void;
    placeholder?: string;
    disabled?: boolean;
    minLength?: number;
    maxLength?: number;
    autoComplete?: "current-password" | "new-password";
}

export default function PasswordInput({
    id,
    name,
    label,
    value,
    onChange,
    placeholder,
    disabled = false,
    minLength = 12,
    maxLength,
    autoComplete = "new-password",
}: PasswordInputProps) {
    const [showPassword, setShowPassword] = useState(false);

    return (
        <div className="w-full">
            <label htmlFor={id} className="mb-2 block text-sm font-medium text-black">
                {label}
            </label>

            <div className="relative">
                <input
                    id={id}
                    name={name}
                    type={showPassword ? "text" : "password"}
                    autoComplete={autoComplete}
                    required
                    minLength={minLength}
                    maxLength={maxLength}
                    value={value}
                    onChange={onChange}
                    placeholder={placeholder}
                    disabled={disabled}
                    className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 pr-12 text-sm text-black outline-none transition-colors placeholder:text-gray-400 focus:border-black focus:ring-1 focus:ring-black disabled:cursor-not-allowed disabled:opacity-50"
                />

                <button
                    type="button"
                    aria-label={showPassword ? "Hide password" : "Show password"}
                    aria-pressed={showPassword}
                    aria-controls={id}
                    onClick={() => setShowPassword((previous) => !previous)}
                    disabled={disabled}
                    className="absolute inset-y-0 right-0 flex w-12 cursor-pointer items-center justify-center rounded-r-lg text-gray-500 transition-colors hover:text-black focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-black disabled:cursor-not-allowed disabled:opacity-50"
                >
                    {showPassword ? (
                        <EyeOff size={19} aria-hidden="true" />
                    ) : (
                        <Eye size={19} aria-hidden="true" />
                    )}
                </button>
            </div>
        </div>
    );
}