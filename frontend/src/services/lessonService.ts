import api from './api';

export const getLessons = async () => {
  const response = await api.get('/lessons/');
  return response.data;
};

export const getLessonById = async (lessonId: number) => {
  const response = await api.get(`/lessons/${lessonId}`);
  return response.data;
};

export const createLesson = async (userId: number, data: any) => {
  const response = await api.post(`/lessons/${userId}`, data);
  return response.data;
};

export const updateLesson = async (lessonId: number, userId: number, data: any) => {
  const response = await api.put(`/lessons/${lessonId}/${userId}`, data);
  return response.data;
};

export const deleteLesson = async (lessonId: number, userId: number) => {
  const response = await api.delete(`/lessons/${lessonId}/${userId}`);
  return response.data;
};
