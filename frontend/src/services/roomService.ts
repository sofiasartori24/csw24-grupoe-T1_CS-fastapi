import api from './api';

export const getRooms = async () => {
  const response = await api.get('/rooms/');
  return response.data;
};

export const getRoomById = async (roomId: number) => {
  const response = await api.get(`/rooms/${roomId}`);
  return response.data;
};

export const createRoom = async (userId: number, data: any) => {
  const response = await api.post(`/rooms/${userId}`, data);
  return response.data;
};

export const updateRoom = async (roomId: number, userId: number, data: any) => {
  const response = await api.put(`/rooms/${roomId}/${userId}`, data);
  return response.data;
};

export const deleteRoom = async (roomId: number, userId: number) => {
  const response = await api.delete(`/rooms/${roomId}/${userId}`);
  return response.data;
};
