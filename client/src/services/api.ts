import axios, { AxiosError } from "axios";
import { FormData } from "../types";

// Use environment variables with fallback for development
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

// Create axios instance with defaults
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  // Add withCredentials for CORS requests
  withCredentials: true,
});

export const submitForm = async (data: Omit<FormData, "id" | "createdAt">) => {
  try {
    // Log the data being sent to the server
    console.log("Submitting form data:", data);

    // First check if we need to perform a preflight to set CORS
    if (typeof window !== "undefined" && window.location.origin !== API_URL) {
      // Perform a preflight request
      await apiClient.options("/submissions/");
    }

    const response = await apiClient.post("/submissions/", data);
    return response.data;
  } catch (error: unknown) {
    console.error("Error submitting form:", error);
    // Log more details if available
    if (error instanceof AxiosError && error.response) {
      console.error("Response data:", error.response.data);
      console.error("Response status:", error.response.status);
      console.error("Response headers:", error.response.headers);
    }
    throw error;
  }
};

export const getAllSubmissions = async () => {
  try {
    const response = await apiClient.get("/submissions/");
    return response.data;
  } catch (error: unknown) {
    console.error("Error fetching submissions:", error);
    // Log more details if available
    if (error instanceof AxiosError && error.response) {
      console.error("Response data:", error.response.data);
      console.error("Response status:", error.response.status);
    }
    throw error;
  }
};
