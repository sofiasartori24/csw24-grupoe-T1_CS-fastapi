import api from './api';

export const getReservations = async () => {
  const response = await api.get('/reservations/');
  return response.data;
};

export const getReservationById = async (reservationId: number) => {
  const response = await api.get(`/reservations/${reservationId}`);
  return response.data;
};

export const createReservation = async (userId: number, data: any) => {
  const response = await api.post(`/reservations/make_reservation/${userId}`, data);
  return response.data;
};



export const deleteReservation = async (reservationId: number, userId: number) => {
  const response = await api.delete(`/reservations/cancel_reservation/${reservationId}/${userId}`);
  return response.data;
};
