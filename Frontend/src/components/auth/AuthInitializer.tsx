import {
    useEffect,
    type ReactNode,
} from "react";

import {
    useAppDispatch,
    useAppSelector,
} from "../../app/hooks";

import {
    restoreSessionThunk,
    sessionInvalidated,
} from "../../features/auth/slices/authSlice";

import {
    AUTH_STORAGE_KEY,
    tokenStore,
} from "../../features/auth/services/tokenStore";

interface AuthInitializerProps {
    children: ReactNode;
}

export default function AuthInitializer({
    children,
}: AuthInitializerProps) {
    const dispatch = useAppDispatch();

    const {
        authInitialized,
        authInitializing,
    } = useAppSelector((state) => state.auth);

    useEffect(() => {
        void dispatch(restoreSessionThunk());
    }, [dispatch]);

    useEffect(() => {
        const handleStorageChange = (event: StorageEvent) => {
            if (event.storageArea !== localStorage) {
                return;
            }

            if (
                event.key !== AUTH_STORAGE_KEY &&
                event.key !== null
            ) {
                return;
            }

            if (!tokenStore.hasTokens()) {
                dispatch(sessionInvalidated());
                return;
            }

            void dispatch(restoreSessionThunk());
        };

        window.addEventListener("storage", handleStorageChange);

        return () => {
            window.removeEventListener(
                "storage",
                handleStorageChange
            );
        };
    }, [dispatch]);

    if (!authInitialized || authInitializing) {
        return (
            <div className="flex min-h-screen items-center justify-center">
                <div className="flex items-center gap-3">
                    <div className="h-6 w-6 animate-spin rounded-full border-2 border-gray-300 border-t-blue-600" />

                    <p className="text-sm text-gray-600">
                        Restoring session...
                    </p>
                </div>
            </div>
        );
    }

    return <>{children}</>;
}