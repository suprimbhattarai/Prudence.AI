import logo from "../../assets/logo/logo.png";

interface LoadingProps {
    variant?: "page" | "inline";
    message?: string;
}

export default function Loading({
    variant = "page",
    message = "Loading Prudence AI...",
}: LoadingProps) {
    const isPage = variant === "page";

    return (
        <div
            role="status"
            aria-live="polite"
            className={`
                flex items-center justify-center
                bg-white text-black
                ${isPage
                    ? "min-h-dvh w-full px-4"
                    : "w-full py-8"
                }
            `}
        >
            <div className="flex flex-col items-center gap-5 text-center">
                <div className="relative flex items-center justify-center">
                    <div
                        aria-hidden="true"
                        className="
                            absolute h-24 w-24 rounded-full
                            border-2 border-gray-200
                            border-t-black
                            animate-spin
                            motion-reduce:animate-none
                        "
                    />

                    <img
                        src={logo}
                        alt=""
                        className="
                            h-16 w-16 rounded-lg object-contain
                            animate-pulse
                            motion-reduce:animate-none
                        "
                    />
                </div>

                <div className="space-y-1">
                    <p className="text-sm font-semibold tracking-wide">
                        Prudence AI
                    </p>

                    <p className="text-xs text-gray-500">
                        {message}
                    </p>
                </div>

                <span className="sr-only">
                    Please wait.
                </span>
            </div>
        </div>
    );
}