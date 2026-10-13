import {
    createAction,
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
};


// ---------------------------------------
// Register User
// ---------------------------------------

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


// ---------------------------------------
// Login User + Fetch Current Account
// ---------------------------------------

export const loginUserThunk = createAsyncThunk<
    AuthUser,
    LoginRequest,
    { rejectValue: string }
>(
    "auth/login",
    async (credentials, { rejectWithValue }) => {
        try {
            // Authenticate through FastAPI
            const loginResponse = await loginUser(credentials);

            // Validate token response
            if (
                !loginResponse.access_token ||
                !loginResponse.refresh_token ||
                loginResponse.token_type?.toLowerCase() !== "bearer"
            ) {
                throw new Error("Invalid authentication response.");
            }

            // Store tokens in memory
            tokenStore.setTokens(
                loginResponse.access_token,
                loginResponse.refresh_token
            );

            // Fetch authenticated user from FastAPI
            const currentUser = await getCurrentUser();

            // Validate account status
            if (!currentUser.is_active) {
                throw new Error("Your account is inactive.");
            }

            if (!currentUser.is_verified) {
                throw new Error("Your account is awaiting verification.");
            }

            return currentUser;
        } catch (error) {
            // Remove tokens if authentication fails
            tokenStore.clearTokens();

            return rejectWithValue(
                error instanceof Error
                    ? error.message
                    : "Login failed"
            );
        }
    }
);


// ---------------------------------------
// Logout Action
// ---------------------------------------

export const logout = createAction("auth/logout");


// ---------------------------------------
// Auth Slice
// ---------------------------------------

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
    },

    extraReducers: (builder) => {
        builder

            // ---------------------------------------
            // Registration Pending
            // ---------------------------------------

            .addCase(registerUserThunk.pending, (state) => {
                state.loading = true;
                state.success = false;
                state.error = null;
            })

            // Registration Successful
            .addCase(registerUserThunk.fulfilled, (state) => {
                state.loading = false;
                state.success = true;
                state.error = null;
            })

            // Registration Failed
            .addCase(registerUserThunk.rejected, (state, action) => {
                state.loading = false;
                state.success = false;
                state.error = action.payload ?? "Registration failed";
            })

            // ---------------------------------------
            // Login Pending
            // ---------------------------------------

            .addCase(loginUserThunk.pending, (state) => {
                state.loginLoading = true;
                state.loginError = null;
                state.user = null;
                state.isAuthenticated = false;
            })

            // Login Successful
            .addCase(loginUserThunk.fulfilled, (state, action) => {
                state.loginLoading = false;
                state.loginError = null;
                state.user = action.payload;
                state.isAuthenticated = true;
            })

            // Login Failed
            .addCase(loginUserThunk.rejected, (state, action) => {
                state.loginLoading = false;
                state.loginError = action.payload ?? "Login failed";
                state.user = null;
                state.isAuthenticated = false;
            })

            // ---------------------------------------
            // Logout
            // ---------------------------------------

            .addCase(logout, (state) => {
                state.user = null;
                state.isAuthenticated = false;
                state.loginLoading = false;
                state.loginError = null;
            });
    },
});


// ---------------------------------------
// Export Actions
// ---------------------------------------

export const {
    resetRegistrationState,
    clearLoginError,
} = authSlice.actions;


// ---------------------------------------
// Export Reducer
// ---------------------------------------

export default authSlice.reducer;