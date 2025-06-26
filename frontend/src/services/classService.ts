import api from './api';

export const getClasses = async () => {
  const response = await api.get('/classes/');
  return response.data;
};

export const getClassById = async (classId: number) => {
  const response = await api.get(`/classes/${classId}`);
  return response.data;
};

export const createClass = async (userId: number, data: any) => {
  const response = await api.post(`/classes/${userId}`, data);
  return response.data;
};

export const updateClass = async (
  classId: number,
  userId: number,
  classData: {
    semester: string;
    schedule: string;
    vacancies: number;
    discipline_id: number;
    professor_id: number;
  }
) => {
  const payload = {
    class_update: classData,
    user: {
      id: userId,
      email: "atualizado@email.com",
      name: "Esse pode ter sido atualizado",
      birth_date: "2025-06-23",
      gender: "F",
      profile: {
        id: 3,
        name: "Coordinator"
      }
    }
  };

  const response = await api.put(`/classes/${classId}/${userId}`, payload);
  return response.data;
};


export const deleteClass = async (
  classId: number,
  userId: number
) => {
  const payload = {
    id: userId,
    email: "atualizado@email.com",
    name: "Esse pode ter sido atualizado",
    birth_date: "2025-06-23",
    gender: "F",
    profile: {
      id: 3,
      name: "Coordinator"
    }
  };

  const response = await api.delete(`/classes/${classId}/${userId}`, {
    data: payload
  });

  return response.data;
};


