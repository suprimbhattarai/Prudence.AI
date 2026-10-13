interface AuthTokens {
    accessToken: string;
    refreshToken: string;
}

let tokens: AuthTokens | null = null;

export const tokenStore = {
    setTokens(accessToken: string, refreshToken: string): void {
        tokens = {
            accessToken,
            refreshToken,
        };
    },

    getAccessToken(): string | null {
        return tokens?.accessToken ?? null;
    },

    clearTokens(): void {
        tokens = null;
    },
};