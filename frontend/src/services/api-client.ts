import axios, { AxiosError } from "axios";
import { HttpMethods } from "@/enums/paths";

async function handleRequest<T>(
  url: string,
  method: HttpMethods,
  config: any = {}
): Promise<T> {
  const apiBaseUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";

  const headers = {
    ...config.headers,
  };

  try {
    const response = await axios({
      url: `${apiBaseUrl}${url}`,
      method,
      ...config,
      headers,
    });

    return response.data as T;
  } catch (error) {
    const err = error as AxiosError;
    throw error;
  }
}

export { handleRequest };
