import { Route, Routes } from "react-router-dom";

import ExplorePage from "../pages/explore/ExplorePage";
import WelcomePage from "../pages/explore/WelcomePage";

import LoginPage from "../pages/auth/LoginPage";
import RegisterPage from "../pages/auth/RegisterPage";

import NotFoundPage from "../pages/errors/NotFoundPage";

import ProtectedRoute from "./ProtectedRoute";
import PublicOnlyRoute from "./PublicOnlyRoute";

export default function AppRoutes() {
    return (
        <Routes>
            <Route path="/" element={<ExplorePage />} />

            <Route element={<PublicOnlyRoute />}>
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
            </Route>

            <Route element={<ProtectedRoute />}>
                <Route path="/welcome" element={<WelcomePage />} />
            </Route>

            <Route path="*" element={<NotFoundPage />} />
        </Routes>
    );
}