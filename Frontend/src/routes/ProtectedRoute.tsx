import {
    Navigate,
    Outlet,
    useLocation,
} from "react-router-dom";

import { useAppSelector } from "../app/hooks";

export default function ProtectedRoute() {
    const location = useLocation();

    const { isAuthenticated, user } = useAppSelector(
        (state) => state.auth
    );

    if (!isAuthenticated || !user) {
        return (
            <Navigate
                to="/login"
                state={{ from: location }}
                replace
            />
        );
    }

    return <Outlet />;
}