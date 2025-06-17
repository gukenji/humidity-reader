export interface PlantPostRequest {
  name: string | null;
  moisture_threshold: number | null;
  check_interval: number | null;
}

export interface PlantPostResponse extends PlantPostRequest {
  id: number;
}

export interface GetAllPlantsResponse {
  plants: PlantPostResponse[];
}
