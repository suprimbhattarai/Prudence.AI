import {
    httpClient,
    authenticatedHttpClient,
} from "../../../services/api/httpClient";

import type {
    RegisterRequest,
    LoginRequest,
    LoginResponse,
    AuthUser,
} from "../types/auth.types";

export async function registerUser(
    userData: RegisterRequest
): Promise<unknown> {
    return httpClient<unknown>("/api/v1/auth/register", {
        method: "POST",
        body: JSON.stringify(userData),
    });
}

export async function loginUser(
    credentials: LoginRequest
): Promise<LoginResponse> {
    return httpClient<LoginResponse>("/api/v1/auth/login", {
        method: "POST",
        body: JSON.stringify(credentials),
    });
}

export async function getCurrentUser(): Promise<AuthUser> {
    return authenticatedHttpClient<AuthUser>("/api/v1/auth/me", {
        method: "GET",
    });
}