import { handleRequest } from "@/services/api-client";
import { ApiRoutes, HttpMethods } from "@/enums/paths";
import { GetHumiditiesResponse } from "./types";

export async function getHumidities(
  start_date: string,
  end_date: string
): Promise<GetHumiditiesResponse> {
  return handleRequest<GetHumiditiesResponse>(
    `${ApiRoutes.HUMIDITY}/data?start_date=${start_date}&end_date=${end_date}`,
    HttpMethods.GET
  );
}
