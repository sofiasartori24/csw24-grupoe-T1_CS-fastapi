import api from './api';

const endpoint = '/profiles/';

export const getProfiles = async () => {
  const response = await api.get(endpoint);
  return response.data;
};

export const getProfileById = async (id: number) => {
  const response = await api.get(`${endpoint}/${id}`);
  return response.data;
};

export const createProfile = async (userId: number, data: any) => {
  const response = await api.post(`${endpoint}/${userId}`, data);
  return response.data;
};

export const updateProfile = async (profileId: number, userId: number, data: any) => {
  const response = await api.put(`${endpoint}/${profileId}/${userId}`, data);
  return response.data;
};

export const deleteProfile = async (profileId: number, userId: number) => {
  const response = await api.delete(`${endpoint}/${profileId}/${userId}`);
  return response.data;
};
