import {
  PlantPostRequest,
  PlantPostResponse,
  GetAllPlantsResponse,
} from "./types";
import { handleRequest } from "@/services/api-client";
import { ApiRoutes, HttpMethods } from "@/enums/paths";

export async function createPlant(
  data: PlantPostRequest
): Promise<PlantPostResponse> {
  return handleRequest<PlantPostResponse>(ApiRoutes.PLANT, HttpMethods.POST, {
    data: data,
  });
}

export async function getPlantById(id: number): Promise<PlantPostResponse> {
  return handleRequest<PlantPostResponse>(
    `${ApiRoutes.PLANT}/${id}`,
    HttpMethods.GET
  );
}

export async function updatePlant(
  id: number,
  data: PlantPostRequest
): Promise<any> {
  return handleRequest<PlantPostResponse>(
    `${ApiRoutes.PLANT}/${id}`,
    HttpMethods.PUT,
    { data: data }
  );
}

export async function deletePlant(id: number): Promise<PlantPostResponse> {
  return handleRequest<PlantPostResponse>(
    `${ApiRoutes.PLANT}/${id}`,
    HttpMethods.DELETE
  );
}

export async function getPlants(): Promise<GetAllPlantsResponse> {
  return handleRequest<GetAllPlantsResponse>(
    `${ApiRoutes.PLANT}/`,
    HttpMethods.GET
  );
}
