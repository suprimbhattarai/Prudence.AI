import {
    createAsyncThunk,
    createSlice,
} from "@reduxjs/toolkit";

import { getAvailableOrganizations } from "../services/organizationApi";

import type { Organization } from "../types/organization.types";

interface OrganizationState {
    organizations: Organization[];
    loading: boolean;
    error: string | null;
}

const initialState: OrganizationState = {
    organizations: [],
    loading: false,
    error: null,
};

export const fetchOrganizations = createAsyncThunk<
    Organization[],
    void,
    { rejectValue: string }
>(
    "organizations/fetchAvailable",
    async (_, { rejectWithValue }) => {
        try {
            return await getAvailableOrganizations();
        } catch (error) {
            return rejectWithValue(
                error instanceof Error
                    ? error.message
                    : "Failed to load organizations"
            );
        }
    }
);

const organizationSlice = createSlice({
    name: "organizations",
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(fetchOrganizations.pending, (state) => {
                state.loading = true;
                state.error = null;
            })

            .addCase(fetchOrganizations.fulfilled, (state, action) => {
                state.loading = false;
                state.organizations = action.payload;
            })

            .addCase(fetchOrganizations.rejected, (state, action) => {
                state.loading = false;
                state.error =
                    action.payload ?? "Unable to fetch organizations";
            });
    },
});

export default organizationSlice.reducer;