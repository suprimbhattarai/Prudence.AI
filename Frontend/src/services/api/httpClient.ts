import { tokenStore } from "../../features/auth/services/tokenStore";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export class ApiError extends Error {
    public readonly status: number;

    constructor(message: string, status: number) {
        super(message);

        this.name = "ApiError";
        this.status = status;
    }
}

function getErrorMessage(data: unknown): string {
    if (typeof data !== "object" || data === null || !("detail" in data)) {
        return "An unexpected error occurred.";
    }

    const detail = data.detail;

    if (typeof detail === "string") {
        return detail;
    }

    if (Array.isArray(detail)) {
        const messages = detail
            .map((error: unknown) => {
                if (typeof error !== "object" || error === null || !("msg" in error)) {
                    return null;
                }

                return typeof error.msg === "string" ? error.msg : null;
            })
            .filter((message): message is string => message !== null);

        return messages.join(", ") || "Validation failed.";
    }

    return "An unexpected error occurred.";
}

export async function httpClient<T>(
    endpoint: string,
    options: RequestInit = {}
): Promise<T> {
    let response: Response;

    try {
        const headers = new Headers(options.headers);

        if (options.body && !headers.has("Content-Type")) {
            headers.set("Content-Type", "application/json");
        }

        response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers,
        });
    } catch {
        throw new Error("Cannot connect to the server. Please check your connection.");
    }

    if (!response.ok) {
        const errorData: unknown = await response.json().catch(() => null);

        throw new ApiError(getErrorMessage(errorData), response.status);
    }

    if (response.status === 204) {
        return undefined as T;
    }

    const text = await response.text();

    return (text ? JSON.parse(text) : undefined) as T;
}

export async function authenticatedHttpClient<T>(
    endpoint: string,
    options: RequestInit = {}
): Promise<T> {
    const accessToken = tokenStore.getAccessToken();

    if (!accessToken) {
        throw new ApiError("Authentication required. Please log in.", 401);
    }

    const headers = new Headers(options.headers);

    headers.set("Authorization", `Bearer ${accessToken}`);

    return httpClient<T>(endpoint, {
        ...options,
        headers,
    });
}