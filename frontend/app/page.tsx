'use client';
import { useEffect, useState } from 'react';
type Task = { id: number; title: string };
const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState('');
  const [error, setError] = useState('');
  async function load() {try {const r = await fetch(`${API}/api/tasks`); if (!r.ok) throw Error('Unable to load tasks'); setTasks(await r.json()); setError('');} catch(e) {setError(String(e));}}
  useEffect(() => {void load();}, []);
  async function add(e: React.FormEvent) {e.preventDefault(); if (!title.trim()) return; try {const r = await fetch(`${API}/api/tasks`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({title:title.trim()})}); if (!r.ok) throw Error('Unable to add task'); setTitle(''); await load();} catch(e) {setError(String(e));}}
  return <main><h1>Coditude Task Manager</h1><p>Next.js + FastAPI + PostgreSQL demo</p><form onSubmit={add}><input aria-label="Task title" value={title} onChange={e=>setTitle(e.target.value)} placeholder="Enter a task" maxLength={200} style={{padding:10,width:'65%'}}/> <button type="submit" style={{padding:10}}>Add Task</button></form>{error && <p role="alert" style={{color:'crimson'}}>{error}</p>}<h2>Tasks</h2><ul>{tasks.map(t=><li key={t.id}>{t.title}</li>)}</ul></main>;
}
