import api from './api';

export const getBuildings = async () => {
  const response = await api.get('/buildings/');
  return response.data;
};

export const getBuildingById = async (buildingId: number) => {
  const response = await api.get(`/buildings/${buildingId}`);
  return response.data;
};

export const createBuilding = async (userId: number, data: any) => {
  const response = await api.post(`/buildings/${userId}`, data);
  return response.data;
};

export const updateBuilding = async (buildingId: number, userId: number, data: any) => {
  const response = await api.put(`/buildings/${buildingId}/${userId}`, data);
  return response.data;
};

export const deleteBuilding = async (buildingId: number, userId: number) => {
  const response = await api.delete(`/buildings/${buildingId}/${userId}`);
  return response.data;
};
