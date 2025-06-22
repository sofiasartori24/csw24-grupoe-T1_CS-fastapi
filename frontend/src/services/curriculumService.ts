import api from './api';

export const getCurriculums = async () => {
  const response = await api.get('/curriculums/');
  return response.data;
};

export const getCurriculumById = async (curriculumId: number) => {
  const response = await api.get(`/curriculums/${curriculumId}`);
  return response.data;
};

export const createCurriculum = async (userId: number, data: any) => {
  const response = await api.post(`/curriculums/${userId}`, data);
  return response.data;
};

export const updateCurriculum = async (curriculumId: number, userId: number, data: any) => {
  const response = await api.put(`/curriculums/${curriculumId}/${userId}`, data);
  return response.data;
};

export const deleteCurriculum = async (curriculumId: number, userId: number) => {
  const response = await api.delete(`/curriculums/${curriculumId}/${userId}`);
  return response.data;
};
