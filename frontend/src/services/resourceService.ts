// services/resourceService.ts
import api from './api';

export const getResources = async () => {
  const response = await api.get('/resources/');
  return response.data;
};

export const getResourceById = async (id: number) => {
  const response = await api.get(`/resources/${id}`);
  return response.data;
};

export const createResource = async (userId: number, data: any) => {
  const response = await api.post(`/resources/${userId}`, data);
  return response.data;
};

export const updateResource = async (resourceId: number, userId: number, data: any) => {
  const response = await api.put(`/resources/${resourceId}/${userId}`, data);
  return response.data;
};

export const deleteResource = async (resourceId: number, userId: number) => {
  const response = await api.delete(`/resources/${resourceId}/${userId}`);
  return response.data;
};
