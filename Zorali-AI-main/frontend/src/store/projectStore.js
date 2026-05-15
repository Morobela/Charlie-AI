import { create } from 'zustand'
import { apiGet, apiPost } from '../api/httpClient'

export const useProjectStore = create((set) => ({
  projects: [],
  selectedProjectId: null,
  async loadProjects() {
    const projects = await apiGet('/api/project')
    set({ projects, selectedProjectId: projects[0]?.id || null })
  },
  async addProject(name, description = '') {
    const project = await apiPost('/api/project', { name, description })
    set((s) => ({ projects: [...s.projects, project], selectedProjectId: s.selectedProjectId || project.id }))
  },
  selectProject(id) { set({ selectedProjectId: id }) }
}))
