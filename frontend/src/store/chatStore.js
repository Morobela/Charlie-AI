import { create } from 'zustand'
import { apiGet } from '../api/httpClient'

export const useChatStore = create((set) => ({
  messages: [],
  async loadHistory(projectId) {
    if (!projectId) return
    const messages = await apiGet(`/api/project/${projectId}/chats`)
    set({ messages })
  },
  add(msg) { set((s) => ({ messages: [...s.messages, msg] })) }
}))
