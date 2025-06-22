import api from './api';

export const getUsers = async () => {
  const response = await api.get('/users/');
  return response.data;
};

export const getUserById = async (userId: number) => {
  const response = await api.get(`/users/${userId}`);
  return response.data;
};

export const createUser = async (requestingUserId: number, data: any) => {
  const response = await api.post(`/users/${requestingUserId}`, data);
  return response.data;
};

export const updateUser = async (
  userToUpdateId: number,
  requestingUserId: number,
  data: any
) => {
  const response = await api.put(`/users/${userToUpdateId}/${requestingUserId}`, data);
  return response.data;
};

