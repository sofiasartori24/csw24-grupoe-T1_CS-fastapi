import { useEffect, useState } from 'react';
import {
  createUser,
  getUsers,
  deleteUser,
  updateUser,
} from '../services/userService';

const Admin = () => {
  const [users, setUsers] = useState<any[]>([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [birthDate, setBirthDate] = useState('');
  const [gender, setGender] = useState('');
  const [role, setRole] = useState(3); // 3 = Professor
  const [editingUserId, setEditingUserId] = useState<number | null>(null);
  const [adminId] = useState(1); // ID do usuário administrador, fixo para este exemplo
  const [professorId] = useState(3); // ID do usuário professor, fixo para este exemplo

  const fetchUsers = async () => {
    try {
      const data = await getUsers();
      setUsers(data);
    } catch (error) {
      console.error('Erro ao buscar usuários:', error);
    }
  };

  const handleCreateOrUpdateUser = async () => {
    if (!name.trim()) return;

    const userData = {
      name,
      email,
      birth_date: birthDate,
      gender,
      profile_id: professorId,
    };

    try {
      if (editingUserId) {
        await updateUser( editingUserId,adminId, userData); // 1 = admin
      } else {
        await createUser(adminId, userData); // 1 = admin
      }

      resetForm();
      fetchUsers();
    } catch (error) {
      console.error('Erro ao salvar usuário:', error);
    }
  };

  const handleDeleteUser = async (userId: number) => {
    try {
      await deleteUser( userId,adminId);
      fetchUsers();
    } catch (error) {
      console.error('Erro ao excluir usuário:', error);
    }
  };

  const handleEditUser = (user: any) => {
    setEditingUserId(user.id);
    setName(user.name);
    setEmail(user.email);
    setBirthDate(user.birth_date);
    setGender(user.gender);
    setRole(user.profile_id);
  };

  const resetForm = () => {
    setName('');
    setEmail('');
    setBirthDate('');
    setGender('');
    setRole(3);
    setEditingUserId(null);
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Painel do Administrador</h2>

      <h4>{editingUserId ? 'Editar usuário' : 'Criar novo usuário (professor)'}</h4>
      <input
        type="text"
        placeholder="Nome"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="date"
        placeholder="Data de nascimento"
        value={birthDate}
        onChange={(e) => setBirthDate(e.target.value)}
      />
      <input
        type="text"
        placeholder="Gênero"
        value={gender}
        onChange={(e) => setGender(e.target.value)}
      />
      <button onClick={handleCreateOrUpdateUser}>
        {editingUserId ? 'Atualizar' : 'Criar'}
      </button>
      {editingUserId && <button onClick={resetForm}>Cancelar</button>}

      <h4 style={{ marginTop: '2rem' }}>Usuários cadastrados</h4>
      <ul>
        {users.map((user: any) => (
          <li key={user.id}>
            {user.name} ({user.email}){' '}
            <button onClick={() => handleEditUser(user)}>Editar</button>{' '}
            <button onClick={() => handleDeleteUser(user.id)}>Excluir</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Admin;
