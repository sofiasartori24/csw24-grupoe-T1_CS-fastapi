// src/pages/Coordenador.tsx
import React, { useEffect, useState } from 'react';
import {
  getClasses,
  createClass,
  updateClass,
  deleteClass
} from '../services/classService';
import { getDisciplines } from '../services/disciplineService';
import { getUsers } from '../services/userService';

const COORDINATOR_ID = 2;
const COORDINATOR_PROFILE_ID = 3; // id do perfil do coordenador

const Coordenador = () => {
  const [classes, setClasses] = useState([]);
  const [semester, setSemester] = useState('');
  const [schedule, setSchedule] = useState('');
  const [vacancies, setVacancies] = useState(0);
  const [disciplineId, setDisciplineId] = useState<number | ''>('');
  const [professorId, setProfessorId] = useState<number | ''>('');
  const [editingId, setEditingId] = useState<number | null>(null);

  const [disciplines, setDisciplines] = useState([]);
  const [professors, setProfessors] = useState([]);

  const fetchClasses = async () => {
    const data = await getClasses();
    setClasses(data);
  };

  const fetchOptions = async () => {
    const allDisciplines = await getDisciplines();
    const allProfessors = await getUsers();
    setDisciplines(allDisciplines);
    setProfessors(allProfessors);
  };

  useEffect(() => {
    fetchClasses();
    fetchOptions();
  }, []);

  const resetForm = () => {
    setSemester('');
    setSchedule('');
    setVacancies(0);
    setDisciplineId('');
    setProfessorId('');
    setEditingId(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();

  // Validação extra para garantir que as opções foram selecionadas
  if (disciplineId === '' || professorId === '') {
    alert('Por favor, selecione uma disciplina e um professor.');
    return;
  }

  const classData = {
    semester,
    schedule,
    vacancies,
    discipline_id: Number(disciplineId),
    professor_id: Number(professorId),
  };

  try {
    if (editingId !== null) {
      await updateClass(editingId, COORDINATOR_ID, classData);
    } else {
      await createClass(COORDINATOR_ID, classData);
    }

    resetForm();
    fetchClasses();
  } catch (err) {
    console.error('Erro ao salvar turma:', err);
  }
};




  const handleEdit = (classObj: any) => {
    setSemester(classObj.semester);
    setSchedule(classObj.schedule);
    setVacancies(classObj.vacancies);
    setDisciplineId(classObj.discipline.id);
    setProfessorId(classObj.professor.id);
    setEditingId(classObj.id);
  };

  const handleDelete = async (classId: number) => {
    try {
      await deleteClass(classId, COORDINATOR_ID);
      fetchClasses();
    } catch (err) {
      console.error('Erro ao excluir turma:', err);
    }
  };

  return (
    <div className="container">
      <h1>Painel do Coordenador</h1>

      <h2>Criar Nova Turma</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Semestre (ex: 2024/1)"
          value={semester}
          onChange={(e) => setSemester(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Horário (ex: Mon-Wed 10:00-12:00)"
          value={schedule}
          onChange={(e) => setSchedule(e.target.value)}
          required
        />
        <input
          type="number"
          placeholder="Número de vagas na turma"
          value={vacancies}
          onChange={(e) => setVacancies(Number(e.target.value))}
          required
        />

        <select
          value={disciplineId}
          onChange={(e) => setDisciplineId(Number(e.target.value))}
          required
        >
          <option value="">Selecione uma disciplina</option>
          {disciplines.map((d: any) => (
            <option key={d.id} value={d.id}>
              {d.name}
            </option>
          ))}
        </select>

        <select
          value={professorId}
          onChange={(e) => setProfessorId(Number(e.target.value))}
          required
        >
          <option value="">Selecione um professor</option>
          {professors.map((p: any) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </select>

        <button type="submit">{editingId ? 'Atualizar' : 'Criar'}</button>
      </form>

      <h2>Turmas Cadastradas</h2>
      <ul>
        {classes.map((c: any) => (
          <li key={c.id}>
            <strong>{c.discipline.name}</strong> - {c.semester} - {c.schedule} - {c.vacancies} vagas
            <br />
            Professor: {c.professor.name}
            <br />
            <button onClick={() => handleEdit(c)}>Editar</button>
            <button onClick={() => handleDelete(c.id)}>Excluir</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Coordenador;
