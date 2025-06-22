import api from './api';

const endpoint = '/resource-types';

export const getResourceTypes = async () => {
  const response = await api.get(endpoint);
  return response.data;
};

export const getResourceTypeById = async (id: number) => {
  const response = await api.get(`${endpoint}/${id}`);
  return response.data;
};

export const createResourceType = async (userId: number, data: any) => {
  const response = await api.post(`${endpoint}/${userId}`, data);
  return response.data;
};

export const updateResourceType = async (typeId: number, userId: number, data: any) => {
  const response = await api.put(`${endpoint}/${typeId}/${userId}`, data);
  return response.data;
};

export const deleteResourceType = async (typeId: number, userId: number) => {
  const response = await api.delete(`${endpoint}/${typeId}/${userId}`);
  return response.data;
};
