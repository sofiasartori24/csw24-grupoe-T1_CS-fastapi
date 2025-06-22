import api from './api';

export const getDisciplines = async () => {
  const response = await api.get('/disciplines/');
  return response.data;
};

export const getDisciplineById = async (disciplineId: number) => {
  const response = await api.get(`/disciplines/${disciplineId}`);
  return response.data;
};

export const createDiscipline = async (userId: number, data: any) => {
  const response = await api.post(`/disciplines/${userId}`, data);
  return response.data;
};

export const updateDiscipline = async (disciplineId: number, userId: number, data: any) => {
  const response = await api.put(`/disciplines/${disciplineId}/${userId}`, data);
  return response.data;
};

export const deleteDiscipline = async (disciplineId: number, userId: number) => {
  const response = await api.delete(`/disciplines/${disciplineId}/${userId}`);
  return response.data;
};
