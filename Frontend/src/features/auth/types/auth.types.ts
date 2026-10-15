export type RegistrationRole = "customer" | "technician";

export type UserRole = RegistrationRole | "admin";

export interface RegisterRequest {
    email: string;
    password: string;
    full_name: string;
    phone: string | null;
    organization_id: number;
    role: RegistrationRole;
}

export interface RegistrationResult {
    message: string;
}

export interface LoginRequest {
    email: string;
    password: string;
}

export interface LoginResponse {
    access_token: string;
    refresh_token: string;
    token_type: "bearer";
}

export interface AuthUser {
    id: number;
    email: string;
    role: UserRole;
    organization_id: number;
    is_active: boolean;
    is_verified: boolean;
}

export interface AuthState {
    // Registration state
    loading: boolean;
    success: boolean;
    error: string | null;

    // Login/session state
    user: AuthUser | null;
    isAuthenticated: boolean;
    loginLoading: boolean;
    loginError: string | null;
    authInitialized: boolean;
    authInitializing: boolean;
}