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
      profile: { id: 3 } // perfil 3 = coordenador
    }
  };

  const response = await api.put(`/classes/${classId}/${userId}`, payload);
  return response.data;
};


export const deleteClass = async (classId: number, userId: number) => {
  const response = await api.delete(`/classes/${classId}/${userId}`);
  return response.data;
};
