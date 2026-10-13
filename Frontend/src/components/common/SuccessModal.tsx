import { useEffect, useId, useRef } from "react";
import { CheckCircle2 } from "lucide-react";

interface ModalAction {
    label: string;
    onClick: () => void;
}

interface SuccessModalProps {
    open: boolean;
    title: string;
    message: string;
    description?: string;
    primaryAction: ModalAction;
    secondaryAction: ModalAction;
}

export default function SuccessModal({
    open,
    title,
    message,
    description,
    primaryAction,
    secondaryAction,
}: SuccessModalProps) {
    const titleId = useId();
    const descriptionId = useId();

    const dialogRef = useRef<HTMLDivElement>(null);
    const primaryButtonRef = useRef<HTMLButtonElement>(null);

    useEffect(() => {
        if (!open) return;

        const previouslyFocusedElement =
            document.activeElement instanceof HTMLElement
                ? document.activeElement
                : null;

        const previousOverflow = document.body.style.overflow;

        document.body.style.overflow = "hidden";
        primaryButtonRef.current?.focus();

        function handleKeyDown(event: KeyboardEvent) {
            if (event.key !== "Tab") return;

            const buttons =
                dialogRef.current?.querySelectorAll<HTMLButtonElement>(
                    "button:not(:disabled)"
                );

            if (!buttons || buttons.length === 0) return;

            const first = buttons[0];
            const last = buttons[buttons.length - 1];

            if (event.shiftKey && document.activeElement === first) {
                event.preventDefault();
                last.focus();
            } else if (!event.shiftKey && document.activeElement === last) {
                event.preventDefault();
                first.focus();
            }
        }

        document.addEventListener("keydown", handleKeyDown);

        return () => {
            document.removeEventListener("keydown", handleKeyDown);
            document.body.style.overflow = previousOverflow;
            previouslyFocusedElement?.focus();
        };
    }, [open]);

    if (!open) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-black/60 px-4 py-6">
            <div
                ref={dialogRef}
                role="dialog"
                aria-modal="true"
                aria-labelledby={titleId}
                aria-describedby={descriptionId}
                className="w-full max-w-md rounded-2xl bg-white p-6 text-center shadow-xl sm:p-8"
            >
                <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-full bg-gray-100">
                    <CheckCircle2 size={36} strokeWidth={1.8} className="text-black" aria-hidden="true" />
                </div>

                <h2 id={titleId} className="text-2xl font-bold tracking-tight text-black sm:text-3xl">
                    {title}
                </h2>

                <p id={descriptionId} className="mt-3 text-sm leading-6 text-gray-600">
                    {message}
                </p>

                {description && (
                    <div className="mt-5 rounded-lg border border-gray-200 bg-gray-50 px-4 py-3 text-sm leading-6 text-gray-700">
                        {description}
                    </div>
                )}

                <div className="mt-7 flex flex-col gap-3 sm:flex-row">
                    <button
                        ref={primaryButtonRef}
                        type="button"
                        onClick={primaryAction.onClick}
                        className="flex min-h-12 w-full cursor-pointer items-center justify-center rounded-lg bg-black px-5 py-3 text-sm font-semibold text-white transition-colors hover:bg-gray-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-black"
                    >
                        {primaryAction.label}
                    </button>

                    <button
                        type="button"
                        onClick={secondaryAction.onClick}
                        className="flex min-h-12 w-full cursor-pointer items-center justify-center rounded-lg border border-gray-300 bg-white px-5 py-3 text-sm font-semibold text-black transition-colors hover:bg-gray-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-black"
                    >
                        {secondaryAction.label}
                    </button>
                </div>
            </div>
        </div>
    );
}