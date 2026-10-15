export interface AuthTokens {
    accessToken: string;
    refreshToken: string;
}

export const AUTH_STORAGE_KEY = "prudence_auth_tokens";

function isAuthTokens(value: unknown): value is AuthTokens {
    if (typeof value !== "object" || value === null) {
        return false;
    }

    const data = value as Record<string, unknown>;

    return (
        typeof data.accessToken === "string" &&
        data.accessToken.length > 0 &&
        typeof data.refreshToken === "string" &&
        data.refreshToken.length > 0
    );
}

function readTokens(): AuthTokens | null {
    try {
        const stored = localStorage.getItem(AUTH_STORAGE_KEY);

        if (!stored) {
            return null;
        }

        const parsed: unknown = JSON.parse(stored);

        if (!isAuthTokens(parsed)) {
            localStorage.removeItem(AUTH_STORAGE_KEY);
            return null;
        }

        return parsed;
    } catch {
        return null;
    }
}

export const tokenStore = {
    setTokens(accessToken: string, refreshToken: string): void {
        const tokens: AuthTokens = {
            accessToken,
            refreshToken,
        };

        localStorage.setItem(
            AUTH_STORAGE_KEY,
            JSON.stringify(tokens)
        );
    },

    getAccessToken(): string | null {
        return readTokens()?.accessToken ?? null;
    },

    getRefreshToken(): string | null {
        return readTokens()?.refreshToken ?? null;
    },

    hasTokens(): boolean {
        return readTokens() !== null;
    },

    clearTokens(): void {
        localStorage.removeItem(AUTH_STORAGE_KEY);
    },
};