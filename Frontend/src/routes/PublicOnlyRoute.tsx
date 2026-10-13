import { Navigate, Outlet } from "react-router-dom";

import { useAppSelector } from "../app/hooks";

export default function PublicOnlyRoute() {
    const { isAuthenticated, user } = useAppSelector(
        (state) => state.auth
    );

    if (isAuthenticated && user) {
        return <Navigate to="/welcome" replace />;
    }

    return <Outlet />;
}