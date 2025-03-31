import axios from "axios";
import { FormData } from "../types";

// Use environment variables with fallback for development
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

// Create axios instance with defaults
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const submitForm = async (data: Omit<FormData, "id" | "createdAt">) => {
  const response = await apiClient.post("/submissions/", data);
  return response.data;
};

export const getAllSubmissions = async () => {
  const response = await apiClient.get("/submissions/");
  return response.data;
};
