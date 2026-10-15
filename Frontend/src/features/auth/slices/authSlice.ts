import {
    createAsyncThunk,
    createSlice,
} from "@reduxjs/toolkit";

import {
    registerUser,
    loginUser,
    getCurrentUser,
} from "../services/authApi";

import { tokenStore } from "../services/tokenStore";

import type {
    AuthState,
    RegisterRequest,
    RegistrationResult,
    LoginRequest,
    AuthUser,
} from "../types/auth.types";

const initialState: AuthState = {
    // Registration
    loading: false,
    success: false,
    error: null,

    // Authentication
    user: null,
    isAuthenticated: false,
    loginLoading: false,
    loginError: null,

    // Authentication initialization
    authInitialized: false,
    authInitializing: false,
};

export const registerUserThunk = createAsyncThunk<
    RegistrationResult,
    RegisterRequest,
    { rejectValue: string }
>(
    "auth/register",
    async (userData, { rejectWithValue }) => {
        try {
            await registerUser(userData);

            return {
                message: "Registration successful.",
            };
        } catch (error) {
            return rejectWithValue(
                error instanceof Error
                    ? error.message
                    : "Registration failed"
            );
        }
    }
);

export const loginUserThunk = createAsyncThunk<
    AuthUser,
    LoginRequest,
    { rejectValue: string }
>(
    "auth/login",
    async (credentials, { rejectWithValue }) => {
        try {
            const loginResponse = await loginUser(credentials);

            if (
                !loginResponse.access_token ||
                !loginResponse.refresh_token ||
                loginResponse.token_type?.toLowerCase() !== "bearer"
            ) {
                throw new Error("Invalid authentication response.");
            }

            tokenStore.setTokens(
                loginResponse.access_token,
                loginResponse.refresh_token
            );

            const currentUser = await getCurrentUser();

            if (!currentUser.is_active) {
                throw new Error("Your account is inactive.");
            }

            if (!currentUser.is_verified) {
                throw new Error("Your account is awaiting verification.");
            }

            return currentUser;
        } catch (error) {
            tokenStore.clearTokens();

            return rejectWithValue(
                error instanceof Error
                    ? error.message
                    : "Login failed"
            );
        }
    }
);

export const restoreSessionThunk = createAsyncThunk<
    AuthUser | null,
    void,
    { rejectValue: string }
>(
    "auth/restoreSession",
    async (_, { rejectWithValue }) => {
        const accessToken = tokenStore.getAccessToken();

        if (!accessToken) {
            return null;
        }

        try {
            const currentUser = await getCurrentUser();

            if (!currentUser.is_active) {
                throw new Error("Your account is inactive.");
            }

            if (!currentUser.is_verified) {
                throw new Error("Your account is awaiting verification.");
            }

            return currentUser;
        } catch (error) {
            if (tokenStore.getAccessToken() === accessToken) {
                tokenStore.clearTokens();
            }

            return rejectWithValue(
                error instanceof Error
                    ? error.message
                    : "Unable to restore session"
            );
        }
    },
    {
        condition: (_, { getState }) => {
            const state = getState() as { auth: AuthState };

            return !state.auth.authInitializing;
        },
    }
);

export const logout = createAsyncThunk(
    "auth/logout",
    async () => {
        tokenStore.clearTokens();
    }
);

const authSlice = createSlice({
    name: "auth",

    initialState,

    reducers: {
        resetRegistrationState: (state) => {
            state.loading = false;
            state.success = false;
            state.error = null;
        },

        clearLoginError: (state) => {
            state.loginError = null;
        },

        sessionInvalidated: (state) => {
            state.user = null;
            state.isAuthenticated = false;
            state.authInitialized = true;
            state.authInitializing = false;
            state.loginLoading = false;
            state.loginError = null;
        },
    },

    extraReducers: (builder) => {
        builder

            .addCase(registerUserThunk.pending, (state) => {
                state.loading = true;
                state.success = false;
                state.error = null;
            })

            .addCase(registerUserThunk.fulfilled, (state) => {
                state.loading = false;
                state.success = true;
                state.error = null;
            })

            .addCase(registerUserThunk.rejected, (state, action) => {
                state.loading = false;
                state.success = false;
                state.error =
                    action.payload ?? "Registration failed";
            })

            .addCase(loginUserThunk.pending, (state) => {
                state.loginLoading = true;
                state.loginError = null;
                state.user = null;
                state.isAuthenticated = false;
            })

            .addCase(loginUserThunk.fulfilled, (state, action) => {
                state.loginLoading = false;
                state.loginError = null;

                state.user = action.payload;
                state.isAuthenticated = true;
                state.authInitialized = true;
            })

            .addCase(loginUserThunk.rejected, (state, action) => {
                state.loginLoading = false;
                state.loginError =
                    action.payload ?? "Login failed";

                state.user = null;
                state.isAuthenticated = false;
                state.authInitialized = true;
            })

            .addCase(restoreSessionThunk.pending, (state) => {
                state.authInitializing = true;
            })

            .addCase(restoreSessionThunk.fulfilled, (state, action) => {
                state.authInitializing = false;
                state.authInitialized = true;

                state.user = action.payload;
                state.isAuthenticated = action.payload !== null;
            })

            .addCase(restoreSessionThunk.rejected, (state) => {
                state.authInitializing = false;
                state.authInitialized = true;

                state.user = null;
                state.isAuthenticated = false;
            })

            .addCase(logout.fulfilled, (state) => {
                state.user = null;
                state.isAuthenticated = false;

                state.authInitialized = true;
                state.authInitializing = false;

                state.loginLoading = false;
                state.loginError = null;
            });
    },
});

export const {
    resetRegistrationState,
    clearLoginError,
    sessionInvalidated,
} = authSlice.actions;

export default authSlice.reducer;